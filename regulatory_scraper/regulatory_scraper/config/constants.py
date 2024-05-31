import os

# AWS Configuration
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

# Mailer Configuration
MAILERSEND_API_KEY = os.getenv('MAILERSEND_API_KEY')
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL')

# PostgreSQL - Main Database Configuration
DB_CONFIG_PSQL_MAIN = {
    'type': 'postgres',
    'host': os.getenv('DB_PSQL_HOST'),
    'port': int(os.getenv('DB_PSQL_PORT')),
    'db_name': 'main_db',
    'user': os.getenv('DB_PSQL_USER'),
    'password': os.getenv('DB_PSQL_PASSWORD')
}

# PostgreSQL - Embedding Database Configuration
DB_CONFIG_PSQL_EMBEDDING = {
    'type': 'postgres',
    'host': os.getenv('DB_PSQL_HOST'),
    'port': int(os.getenv('DB_PSQL_PORT')),
    'db_name': 'embedding_db',
    'user': os.getenv('DB_PSQL_USER'),
    'password': os.getenv('DB_PSQL_PASSWORD')
}

# PGVector Connection String
PGVECTOR_CONNECTION = f"postgresql+psycopg://{DB_CONFIG_PSQL_EMBEDDING['user']}:{DB_CONFIG_PSQL_EMBEDDING['password']}@{DB_CONFIG_PSQL_EMBEDDING['host']}:{DB_CONFIG_PSQL_EMBEDDING['port']}/{DB_CONFIG_PSQL_EMBEDDING['db_name']}"

# AWS S3 Bucket Name
S3_BUCKET_NAME = "financial-services-regulations"

# SQLite Database Configuration
DB_CONFIG_SQLITE = {
    'type': 'sqlite',
    'path': 'documents_checksums.db'
}