from itemadapter import ItemAdapter
import hashlib
import boto3
from sqlalchemy.exc import SQLAlchemyError
from boto3.exceptions import Boto3Error
from sqlalchemy.sql import func

from regulatory_scraper.database import DatabaseManager, DocumentBin
from regulatory_scraper.config import DB_CONFIG_PSQL_MAIN, AWS_ACCESS_KEY, S3_BUCKET_NAME, AWS_SECRET_ACCESS_KEY, DB_CONFIG_SQLITE, FCA, FCA_EMBEDDINGS
from regulatory_scraper.utils import extract_text_with_pymupdf

from regulatory_scraper.services import ChecksumService, CategoryService, DocumentService, EmbeddingService

class PDFProcessingPipeline:
    def open_spider(self, spider):
        self.db_manager_psql = DatabaseManager(DB_CONFIG_PSQL_MAIN)
        self.db_manager_psql.establish_connection()

        self.db_manager_sqlite = DatabaseManager(DB_CONFIG_SQLITE)
        self.db_manager_sqlite.establish_connection()

        self.checksum_service = ChecksumService()
        self.category_service = CategoryService()
        self.document_service = DocumentService()
        self.embedding_service = EmbeddingService(collection_name=FCA_EMBEDDINGS)

        self.accessed_documents = set()

        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )

        with self.db_manager_psql.SessionFactory() as session:
            all_checksums = self.checksum_service.get_all_checksums(session)
            self.checksums_dict = {checksum.file_url: checksum.checksum for checksum in all_checksums}

        spider.logger.info("Spider opened and database connections established along with checksums loaded.")

    def process_item(self, item, spider):
        file_url = item['file_url']
        file_path = item['file_path']
        response_body = item['response_body']
        category = item['category']
        spider.logger.debug(f"Starting to process item from URL: {file_url}")

        self.accessed_documents.add(file_url)
        new_checksum = hashlib.md5(response_body).hexdigest()
        spider.logger.debug(f"Checksum calculated: {new_checksum}")

        current_checksum = self.checksums_dict.get(file_url)
        document_entry = None
        keywords = None

        try:
            with self.db_manager_psql.session_scope() as session:
                if current_checksum:
                    if current_checksum == new_checksum:
                        spider.logger.info(f"Skipping {file_path} as it has not been modified.")
                        return None
                    else:
                        spider.logger.debug("Document exists and checksum has changed. Retrieving document...")
                        document_entry = self.document_service.get_document(session, file_url=file_url)
                        if document_entry:
                            spider.logger.debug(f"Deleting embeddings for document ID: {document_entry.id}")
                            self.embedding_service.delete_document_embeddings([document_entry.id])
                            spider.logger.debug("Embeddings deleted successfully.")

                            spider.logger.debug("Updating checksum in the database...")
                            self.checksum_service.update_checksum_by_url(session, file_url, new_checksum)
                            spider.logger.debug("Checksum updated successfully.")
                else:
                    self.checksum_service.add_checksum(session, file_url, new_checksum)

                    spider.logger.debug("Adding new category...")
                    category_entry = self.category_service.get_or_create_category(session, category)
                    session.flush()
                    spider.logger.debug(f"Category {category} added/updated with ID: {category_entry.id}")

                    spider.logger.debug("Adding new document...")
                    document_entry = self.document_service.add_document(session, file_url, file_path, category_entry.id, FCA)
                    session.flush()
                    spider.logger.debug(f"Document added with ID: {document_entry.id}")
                
                if document_entry:
                    self.embedding_service.process_document(response_body, document_entry.id, FCA, file_url)
                    spider.logger.debug("Document embeddings processed and stored.")
            
            """
            # Uploading to S3 outside the session scope to prevent holding the transaction open
            spider.logger.debug("Uploading PDF to S3...")
            self.s3_client.put_object(
                Body=response_body,
                Bucket=S3_BUCKET_NAME,
                Key=file_path,
                ContentType='application/pdf',
                Metadata={
                    'OriginalURL': file_url,
                    'Category': category
                }
            )
            spider.logger.info(f"PDF file {file_path} uploaded to S3 successfully.")
            """
                
        except SQLAlchemyError as e:
            spider.logger.error(f"Database operation failed for URL {file_url}: {str(e)}")
            return None
        except Boto3Error as e:
            spider.logger.error(f"S3 operation failed for {file_path}: {str(e)}")
            return None
        except Exception as e:
            spider.logger.error(f"An unexpected error occurred for URL {file_url}: {str(e)}")
            return None

    def close_spider(self, spider):
        try:
            with self.db_manager_sqlite.session_scope() as session:
                unaccessed_urls = set(self.checksums_dict.keys()) - self.accessed_documents
                for url in unaccessed_urls:
                    existing_entry = session.query(DocumentBin).filter_by(file_url=url).first()
                    if not existing_entry:
                        new_bin_entry = DocumentBin(file_url=url)
                        session.add(new_bin_entry)
                        session.commit()
                        spider.logger.info(f"Document {url} added to bin as it was not accessed.")
        except Exception as e:
            spider.logger.error(f"An unexpected error occurred: {str(e)}")

        self.db_manager_psql.close()
        self.db_manager_sqlite.close()
        spider.logger.info("Spider closed and all database connections terminated.")
