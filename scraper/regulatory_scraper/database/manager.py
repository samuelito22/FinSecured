import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DatabaseManager:
    def __init__(self, configuration):
        self.configuration = configuration
        self.engine = None
        self.SessionFactory = None

    def establish_connection(self):
        """Establishes database connection using the configuration provided."""
        database_url = self._construct_database_url()
        self.engine = create_engine(database_url, echo=False)
        self.SessionFactory = sessionmaker(bind=self.engine)
        
        # Testing the connection
        try:
            with self.SessionFactory() as session:
                session.execute(text("SELECT 1"))
                logging.info(f"Connection to database [{self.configuration['type']}] established successfully!")
        except Exception as error:
            logging.error(f"Failed to connect to database [{self.configuration['type']}]: {str(error)}")
            self.close()

    def _construct_database_url(self):
        """Constructs the database URL based on the type of database."""
        db_type = self.configuration['type']
        if db_type == 'sqlite':
            return f"sqlite:///{self.configuration['path']}"
        elif db_type == 'postgres':
            return self.configuration['path']
        else:
            raise ValueError(f"Unsupported database type: {db_type}")

    @contextmanager
    def session_scope(self):
        """Provide a transactional scope around a series of operations."""
        session = self.SessionFactory()
        try:
            session.begin()
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def close(self):
        """Closes the engine and disposes of any resources."""
        if self.engine:
            self.engine.dispose()
            logging.info("Database engine disposed.")

