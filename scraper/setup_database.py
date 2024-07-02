from regulatory_scraper.config import DB_CONFIG_PSQL_MAIN, DB_CONFIG_SQLITE
from regulatory_scraper.database import DatabaseManager, BasePostgres, BaseSQLite
from sqlalchemy import text
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_database(config):
    db_manager = None
    try:
        db_manager = DatabaseManager(config)
        db_manager.establish_connection()

        # Check which base to use based on the database type
        if config['type'] == 'postgres' and config['db_name'] == 'main_db':
            BasePostgres.metadata.create_all(db_manager.engine)
        elif config['type'] == 'sqlite':
            BaseSQLite.metadata.create_all(db_manager.engine)
        else:
            raise ValueError("Unsupported database type")
        logging.info(f"Database [{config['type']}] set-up completed. Now closing...")

    except Exception as e:
        logging.error("Error happened whilst setting up the database: %s", e)
        if db_manager and hasattr(db_manager, 'session'):
            db_manager.session.rollback()
    finally:
        if db_manager:
            db_manager.close()


if __name__ == '__main__':
    setup_database(DB_CONFIG_PSQL_MAIN)
    setup_database(DB_CONFIG_SQLITE)
