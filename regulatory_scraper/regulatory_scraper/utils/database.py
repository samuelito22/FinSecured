from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

class DatabaseManager:
    def __init__(self, db_config):
        self.db_config = db_config
        self.engine = None
        self.Session = None

    def connect(self):
        db_url = self._get_db_url()
        print(db_url)
        self.engine = create_engine(db_url, echo=False)
        self.Session = sessionmaker(bind=self.engine)

        try:
            with self.Session() as session:
                session.execute(text("SELECT 1"))
            print(f"Database [{self.db_config['type']}] connection successful!")
        except Exception as e:
            print(f"Database [{self.db_config['type']}] connection failed: {str(e)}")

    def _get_db_url(self):
        db_type = self.db_config['type']
        if db_type == 'sqlite':
            db_path = self.db_config['path']
            return f'sqlite:///{db_path}'
        elif db_type == 'postgres':
            db_host = self.db_config['host']
            db_port = self.db_config['port']
            db_name = self.db_config['name']
            db_user = self.db_config['user']
            db_password = self.db_config['password']
            return f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
        else:
            raise ValueError(f"Unsupported database type: {db_type}")

    def execute(self, query, params=None):
        with self.Session() as session:
            return session.execute(text(query), params)

    def commit(self):
        with self.Session() as session:
            session.commit()

    def close(self):
        if self.engine:
            self.engine.dispose()