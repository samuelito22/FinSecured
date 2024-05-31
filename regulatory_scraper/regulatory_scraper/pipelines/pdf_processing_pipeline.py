from itemadapter import ItemAdapter
import hashlib
import boto3

from regulatory_scraper.database.manager import DatabaseManager
from regulatory_scraper.config import DB_CONFIG_SQLITE, DB_CONFIG_PSQL_MAIN, AWS_ACCESS_KEY, S3_BUCKET_NAME, AWS_SECRET_ACCESS_KEY

from regulatory_scraper.services import ChecksumService, CategoryService, DocumentService, EmbeddingService

class PDFProcessingPipeline:
    def open_spider(self, spider):
        self.db_manager_sqlite = DatabaseManager(DB_CONFIG_SQLITE)
        self.db_manager_psql = DatabaseManager(DB_CONFIG_PSQL_MAIN)
        self.db_manager_sqlite.establish_connection()
        self.db_manager_psql.establish_connection()
        self.embedding_service = EmbeddingService()
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )

    def process_item(self, item, spider):
        file_url = item['file_url']
        file_path = item['file_path']
        response_body = item['response_body']

        # Open new sessions for each item
        psql_main_session = self.db_manager_psql.SessionFactory()
        sqlite_session = self.db_manager_sqlite.SessionFactory()

        try:
            # Initialize service instances with the correct session
            checksum_service = ChecksumService(sqlite_session)
            category_service = CategoryService(psql_main_session)
            document_service = DocumentService(psql_main_session)

            # Calculate new checksum
            new_checksum = hashlib.md5(response_body).hexdigest()
            
            # Begin a transaction with the SQLite database
            with sqlite_session.begin():
                # Verify checksum without changing the database state
                checksum_not_changed = checksum_service.verify_checksum(file_url, new_checksum)

                if checksum_not_changed:
                    spider.logger.info(f"Skipping {file_path} as it has not been modified.")
                    # Update last accessed time within the same transaction
                    checksum_service.update_last_accessed(file_url)
                    sqlite_session.close()
                    psql_main_session.close()
                    return None
            
            # Proceed if checksum has changed
            with sqlite_session.begin() as transaction_sqlite, psql_main_session.begin() as transaction_psql:
                # Update checksum by URL
                checksum_service.update_checksum_by_url(file_url, new_checksum)

                # Add to category (if not exists)
                category_name = file_path.split('/')[1]
                category = category_service.get_or_create_category(category_name)
                psql_main_session.flush()
                category_id = category.id

                # Add to documents table
                document = document_service.add_document(file_url, file_path, category_id)
                psql_main_session.flush()
                document_id = document.id

                # Add pdf to s3 document
                self.s3_client.put_object(Body=response_body, Bucket=S3_BUCKET_NAME, Key=file_path)

                # Add embeddings
                self.embedding_service.process_and_store_document_embeddings(response_body, document_id)

            spider.logger.info(f"PDF file with URL {file_url} has been changed or added.")
        except Exception as e:
            spider.logger.error(f"Error occurred when processing {file_path}: {e}")
            # Ensure all transactions are rolled back in case of error
            sqlite_session.rollback()
            psql_main_session.rollback()
            return None
        finally:
            # Always close sessions
            sqlite_session.close()
            psql_main_session.close()

        return item

    def close_spider(self, spider):
        # Close global connections
        self.db_manager_psql.close()
        self.db_manager_sqlite.close()
