import logging
from sqlalchemy.orm import Session
import boto3

from regulatory_scraper.config import DB_CONFIG_PSQL_MAIN, AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY, S3_BUCKET_NAME, DB_CONFIG_SQLITE, FCA, FCA_EMBEDDINGS
from regulatory_scraper.database import DatabaseManager, DocumentChecksum, Document, DocumentBin
from regulatory_scraper.services import EmbeddingService

class CleanupDatabase:
    def __init__(self, config_psql, config_sqlite, collection_name, regulation):
        self.db_manager_psql = DatabaseManager(config_psql)
        self.db_manager_psql.establish_connection()

        self.db_manager_sqlite = DatabaseManager(config_sqlite)
        self.db_manager_sqlite.establish_connection()

        self.regulation = regulation
        self.embedding_service = EmbeddingService(collection_name=collection_name)
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )


    def run_cleanup(self):
        try:
            with self.db_manager_psql.session_scope() as session_psql, self.db_manager_sqlite.session_scope() as session_sqlite:
                self.clean_up_documents_from_bin(session_psql, session_sqlite)
                logging.info("Cleanup process completed successfully.")
                
        except Exception as e:
            logging.error(f"Cleanup process failed: {str(e)}")

    def clean_up_documents_from_bin(self, session_psql: Session, session_sqlite: Session):
        # Fetch all URLs from DocumentBin
        bin_entries = session_sqlite.query(DocumentBin).all()
        if not bin_entries:
            logging.info("No documents in bin to process.")
            return

        urls_to_clean = [entry.file_url for entry in bin_entries]

        # Delete from DocumentChecksum, Document, and vectors
        self.clean_up_documents(session_psql, urls_to_clean)
        self.clean_up_checksums(session_psql)
        self.clean_up_vectors(session_psql)

        # Delete from S3
        self.delete_from_s3()

        # Remove entries from DocumentBin
        num_bin_deleted = session_sqlite.query(DocumentBin).filter(DocumentBin.file_url.in_(urls_to_clean)).delete()
        logging.info(f"Removed {num_bin_deleted} entries from Document Bin.")

    def clean_up_checksums(self, session: Session):
        if self.document_urls:
            num_deleted = session.query(DocumentChecksum).filter(DocumentChecksum.file_url.in_(self.document_urls)).delete(synchronize_session=False)
            logging.info(f"Deleted {num_deleted} checksum entries.")

    def clean_up_documents(self, session: Session, urls: list):
        old_documents = session.query(Document).filter(Document.file_url.in_(urls), Document.regulation == self.regulation)
        self.document_ids = [doc.id for doc in old_documents]
        self.s3_paths = [doc.file_s3_path for doc in old_documents]
        self.document_urls = [doc.file_url for doc in old_documents]
        old_documents.delete(synchronize_session=False)
        num_deleted = len(old_documents)
        logging.info(f"Deleted {num_deleted} documents from PostgreSQL.")

    def clean_up_vectors(self, session: Session):
        if self.document_ids:
            num_deleted = self.embedding_service.delete_documents_embeddings(self.document_ids)
            logging.info(f"Deleted {num_deleted} vectors from embedding service.")

    def delete_from_s3(self):
        max_retries = 3  # Define the maximum number of retries for each delete operation
        backoff_factor = 2  # The factor by which the wait time will increase after each retry

        for s3_path in self.s3_paths:
            retries = 0
            while retries < max_retries:
                try:
                    response = self.s3_client.delete_object(Bucket=S3_BUCKET_NAME, Key=s3_path)
                    logging.info(f"Deleted {s3_path} from S3 bucket.")
                    break  # If the deletion is successful, break out of the retry loop
                except boto3.exceptions.Boto3Error as e:
                    retries += 1
                    wait_time = backoff_factor ** retries  # Exponential backoff
                    logging.warning(f"Attempt {retries} failed to delete {s3_path} from S3: {e}. Retrying in {wait_time} seconds.")
                    time.sleep(wait_time)  # Wait before trying again

            if retries == max_retries:
                logging.error(f"Failed to delete {s3_path} from S3 after {max_retries} attempts.")

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    cleaner = CleanupDatabase(DB_CONFIG_PSQL_MAIN, DB_CONFIG_SQLITE, collection_name=FCA_EMBEDDINGS, regulation=FCA)
    cleaner.run_cleanup()

