from regulatory_scraper.config import DB_CONFIG_SQLITE, DB_CONFIG_PSQL_MAIN
from regulatory_scraper.database import DatabaseManager, DocumentChecksum, Document
from regulatory_scraper.services import EmbeddingService
import logging
from datetime import datetime, timedelta
from langchain_postgres.vectorstores import PGVector

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
cutoff_date = datetime.utcnow() - timedelta(days=7)

class CleanupDatabase:
    def __init__(self, sqlite_config, psql_main_config):
        self.db_manager_sqlite = DatabaseManager(sqlite_config)
        self.db_manager_psql_main = DatabaseManager(psql_main_config)
        self.db_manager_psql_main.establish_connection()
        self.db_manager_sqlite.establish_connection()
        self.embedding_service = EmbeddingService()

    def run_cleanup(self):
        try:
            with self.db_manager_sqlite.SessionFactory() as session_sqlite, session_sqlite.begin():
                checksum_deleted = self.clean_up_checksum(session_sqlite)
                if checksum_deleted > 0:
                    with self.db_manager_psql_main.SessionFactory() as session_psql_main, session_psql_main.begin():
                        if not self.clean_up_documents(session_psql_main):
                            raise Exception("Failed to delete documents, prompting rollback.")
                        # After successfully deleting documents, now delete corresponding vectors
                        self.clean_up_vectors()
                    logging.info("Cleanup process completed successfully.")
                else:
                    logging.info("No checksums to delete.")
        
        except Exception as e:
            logging.error(f"Cleanup process failed: {str(e)}")
            # The sessions automatically rollback due to the exception

    def clean_up_checksum(self, session_sqlite):
        old_documents = session_sqlite.query(DocumentChecksum).filter(DocumentChecksum.last_accessed < cutoff_date)
        self.old_urls = [doc.file_url for doc in old_documents]
        self.document_ids = [doc.id for doc in old_documents]
        num_deleted = old_documents.delete(synchronize_session=False)
        logging.info(f"Deleted {num_deleted} checksum entries.")
        return num_deleted

    def clean_up_documents(self, session_psql):
        if not self.old_urls:
            logging.info("No old document URLs to process for deletion.")
            return False

        num_deleted = session_psql.query(Document).filter(Document.file_url.in_(self.old_urls)).delete(synchronize_session=False)
        logging.info(f"Deleted {num_deleted} documents from PostgreSQL.")
        return True

    def clean_up_vectors(self):
        if not self.document_ids:
            logging.info("No document IDs to process for vector deletion.")
            return
        
        num_deleted = self.embedding_service.delete_documents_embeddings(self.document_ids)

        logging.info(f"Deleted {num_deleted} vectors from pg_vector_store.")

if __name__ == '__main__':
    sqlite_config = DB_CONFIG_SQLITE  # Ensure this is properly configured
    psql_main_config = DB_CONFIG_PSQL_MAIN  # Ensure this is properly configured
    cleaner = CleanupDatabase(sqlite_config, psql_main_config)
    cleaner.run_cleanup()
