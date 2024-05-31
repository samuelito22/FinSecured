from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

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
                print(f"Connection to database [{self.configuration['type']}] established successfully!")
        except Exception as error:
            print(f"Failed to connect to database [{self.configuration['type']}]: {str(error)}")
            self.close()

    def _construct_database_url(self):
        """Constructs the database URL based on the type of database."""
        db_type = self.configuration['type']
        if db_type == 'sqlite':
            return f"sqlite:///{self.configuration['path']}"
        elif db_type == 'postgres':
            return f"postgresql://{self.configuration['user']}:{self.configuration['password']}@" \
                   f"{self.configuration['host']}:{self.configuration['port']}/{self.configuration['db_name']}"
        else:
            raise ValueError(f"Unsupported database type: {db_type}")

    def close(self):
        """Closes the engine and disposes of any resources."""
        if self.engine:
            self.engine.dispose()
            print("Database engine disposed.")
