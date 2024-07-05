import os

# AWS Configuration
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

# PostgreSQL - Main Database Configuration
DB_CONFIG_PSQL_MAIN = {
    'type': 'postgres',
    'path': os.getenv('MAIN_DATABASE_URL'),
}

# AWS S3 Bucket Name
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')

FCA_EMBEDDINGS = "fca_regulatory"
FCA = "FCA"

# SQLite Database Configuration
DB_CONFIG_SQLITE = {
    'type': 'sqlite',
    'path': 'documents_bin.db'
}

COHERE_API_KEY = os.getenv('COHERE_API_KEY')

QDRANT_URL = os.getenv('QDRANT_URL')