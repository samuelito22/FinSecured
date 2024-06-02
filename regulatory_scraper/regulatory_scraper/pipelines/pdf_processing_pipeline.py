from itemadapter import ItemAdapter
import hashlib
import boto3
from sqlalchemy.exc import SQLAlchemyError
from boto3.exceptions import Boto3Error

from regulatory_scraper.database.manager import DatabaseManager
from regulatory_scraper.config import DB_CONFIG_SQLITE, DB_CONFIG_PSQL_MAIN, AWS_ACCESS_KEY, S3_BUCKET_NAME, AWS_SECRET_ACCESS_KEY

from regulatory_scraper.services import ChecksumService, CategoryService, DocumentService, EmbeddingService

class PDFProcessingPipeline:
    def open_spider(self, spider):
        self.db_manager_sqlite = DatabaseManager(DB_CONFIG_SQLITE)
        self.db_manager_psql = DatabaseManager(DB_CONFIG_PSQL_MAIN)
        self.db_manager_sqlite.establish_connection()
        self.db_manager_psql.establish_connection()

        self.checksum_service = ChecksumService()
        self.category_service = CategoryService()
        self.document_service = DocumentService()
        self.embedding_service = EmbeddingService()

        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )
        spider.logger.info("Spider opened and database connections established.")

    def process_item(self, item, spider):
        file_url = item['file_url']
        file_path = item['file_path']
        response_body = item['response_body']
        category = item['category']
        spider.logger.debug(f"Starting to process item from URL: {file_url}")

        checksum_not_changed = False
        checksum_exist = False
        new_checksum = hashlib.md5(response_body).hexdigest()
        spider.logger.debug(f"Checksum calculated: {new_checksum}")

        try:
            with self.db_manager_sqlite.session_scope() as sqlite_session, self.db_manager_psql.session_scope() as psql_session:
                spider.logger.debug("Starting checksum verification...")
                checksum_not_changed, checksum_exist = self.checksum_service.verify_checksum(sqlite_session, file_url, new_checksum)
                spider.logger.debug(f"Checksum verification result - Not Changed: {checksum_not_changed}, Exists: {checksum_exist}")

                if checksum_not_changed and checksum_exist:
                    spider.logger.info(f"Skipping {file_path} as it has not been modified.")
                    return None 

                if checksum_exist and not checksum_not_changed:
                    spider.logger.debug("Document exists and checksum has changed. Retrieving document...")
                    document_entry = self.document_service.get_document(file_url=file_url)
                    if document_entry:
                        spider.logger.debug(f"Deleting embeddings for document ID: {document_entry.id}")
                        self.embedding_service.delete_document_embeddings(document_entry.id)
                        spider.logger.debug("Embeddings deleted successfully.")

                spider.logger.debug("Updating checksum in the database...")
                self.checksum_service.update_checksum_by_url(sqlite_session, file_url, new_checksum)
                spider.logger.debug("Checksum updated successfully.")

                if not checksum_exist:
                    spider.logger.debug("Adding new category...")
                    category_entry = self.category_service.get_or_create_category(psql_session, category)
                    psql_session.flush()
                    spider.logger.debug(f"Category {category} added/updated with ID: {category_entry.id}")

                    spider.logger.debug("Adding new document...")
                    document_entry = self.document_service.add_document(psql_session, file_url, file_path, category_entry.id)
                    psql_session.flush()
                    spider.logger.debug(f"Document added with ID: {document_entry.id}")
                
                spider.logger.debug("Processing and storing document embeddings...")
                self.embedding_service.process_and_store_document_embeddings(response_body, document_entry.id if document_entry else None)
                spider.logger.debug("Document embeddings processed and stored.")

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
        # Close global connections
        self.db_manager_psql.close()
        self.db_manager_sqlite.close()
        spider.logger.info("Spider closed and all database connections terminated.")
