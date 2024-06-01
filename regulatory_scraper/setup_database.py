from regulatory_scraper.config import DB_CONFIG_SQLITE, DB_CONFIG_PSQL_MAIN, DB_CONFIG_PSQL_EMBEDDING
from regulatory_scraper.database import DatabaseManager, BaseSQLite, BasePostgres 
from sqlalchemy import text

def setup_database(config):
    db_manager = None
    try:
        db_manager = DatabaseManager(config)
        db_manager.establish_connection()

        # Check which base to use based on the database type
        if config['type'] == 'sqlite':
            BaseSQLite.metadata.create_all(db_manager.engine)
        elif config['type'] == 'postgres' and config['db_name'] == 'main_db':
            BasePostgres.metadata.create_all(db_manager.engine)
        elif config['type'] == 'postgres' and config['db_name'] == 'embedding_db':
            # Using the engine directly to execute the command
            with db_manager.engine.begin() as conn:  # Use begin() to handle transactions automatically
                conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        else:
            raise ValueError("Unsupported database type")

        print(f"Database [{config['type']}] set-up completed. Now closing...")

    except Exception as e:
        print("Error happened whilst setting up the database:", e)
        # Properly handle rollback if session management is available
        if db_manager and hasattr(db_manager, 'session'):
            db_manager.session.rollback()
    finally:
        if db_manager:
            db_manager.close()

if __name__ == '__main__':
    setup_database(DB_CONFIG_PSQL_MAIN)
    setup_database(DB_CONFIG_SQLITE)
    setup_database(DB_CONFIG_PSQL_EMBEDDING)
