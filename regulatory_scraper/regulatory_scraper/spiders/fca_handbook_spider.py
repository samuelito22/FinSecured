import scrapy
from scrapy.http import Request
import boto3
import os
import hashlib
from regulatory_scraper.utils.email_alert import send_email_alert
from regulatory_scraper.utils.database import DatabaseManager
from langchain_postgres import PGVector
from langchain_postgres.vectorstores import PGVector
import uuid
from datetime import datetime

class FCAHandbookSpider(scrapy.Spider):
    name = 'fca_handbook_spider'
    allowed_domains = ['handbook.fca.org.uk']
    start_urls = ['https://www.handbook.fca.org.uk/handbook']

    def __init__(self, *args, **kwargs):
        super(FCAHandbookSpider, self).__init__(*args, **kwargs)
        self.setup_aws_client()
        self.bucket_name = "financial-services-regulations"
        self.error_log = []
        self.setup_sqlite_database()
        self.setup_postgres_database()

    def setup_aws_client(self):
        access_key_id = os.getenv('AWS_ACCESS_KEY')
        secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        if not access_key_id or not secret_access_key:
            self.logger.critical("AWS credentials are not set properly.")
            return None
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key
        )

    def setup_sqlite_database(self):
        db_config_sqlite = {
            'type': 'sqlite',
            'path': 'documents_checksums.db'
        }
        self.db_manager_sqlite = DatabaseManager(db_config_sqlite)
        self.db_manager_sqlite.connect()
        self.db_manager_sqlite.execute(
            '''
            CREATE TABLE IF NOT EXISTS documents_checksums (
                id TEXT PRIMARY KEY,
                checksum TEXT NOT NULL,
                file_url TEXT UNIQUE NOT NULL,
                last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            '''
        )
        self.db_manager_sqlite.commit()

    def setup_postgres_database(self):
        db_config_psql = {
            'type': 'postgres',
            'host': os.getenv('DB_PSQL_HOST'),
            'port': int(os.getenv('DB_PSQL_PORT')),
            'name': os.getenv('DB_PSQL_NAME'),
            'user': os.getenv('DB_PSQL_USER'),
            'password': os.getenv('DB_PSQL_PASSWORD')
        }

        self.db_manager_psql = DatabaseManager(db_config_psql)
        self.db_manager_psql.connect()
        self.create_postgres_tables()
        self.db_manager_psql.commit()

        pgvector_connection = "postgresql+psycopg://langchain:langchain@localhost:6024/langchain"
        self.embeddings_store = PGVector(connection=pgvector_connection)
        self.embeddings_store.create_table("embeddings")

    def create_postgres_tables(self):
        self.db_manager_psql.execute(
            '''
            CREATE TABLE IF NOT EXISTS documents (
                id UUID PRIMARY KEY,
                file_url TEXT UNIQUE NOT NULL,
                file_s3_path TEXT NOT NULL,
                category_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT NOW(),
                updated_at TIMESTAMP DEFAULT NOW(),
                FOREIGN KEY (category_id) REFERENCES categories (id)
            )
            '''
        )
        self.db_manager_psql.execute(
            '''
            CREATE TABLE IF NOT EXISTS categories (
                id SERIAL PRIMARY KEY,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT NOW(),
                updated_at TIMESTAMP DEFAULT NOW()
            )
            '''
        )

    def parse(self, response):
        section_links = response.css('a[href^="/handbook"]::attr(href)').getall()
        for link in section_links:
            section_url = response.urljoin(link)
            yield Request(section_url, callback=self.parse_section)

    def parse_section(self, response):
        pdf_links = response.css('a[href$=".pdf"]::attr(href)').getall()
        for link in pdf_links:
            pdf_url = response.urljoin(link)
            section = response.url.split('/')
            category_index = section.index('handbook') + 1
            filename = os.path.basename(link)
            file_path = f'handbook/{section[category_index]}/{filename}'
            yield Request(pdf_url, callback=self.save_pdf, meta={'file_url': pdf_url, 'file_path': file_path})

    def save_pdf(self, response):
        file_url = response.meta['file_url']
        file_path = response.meta['file_path']
        self.logger.info(f'Saving PDF from URL: {file_url} to file path: {file_path}')
        try:
            new_checksum = hashlib.md5(response.body).hexdigest()
            old_checksum = self.get_checksum_from_db(file_url)
            if old_checksum == new_checksum:
                self.logger.info(f"Skipping {file_path} as it has not been modified.")
                return

            # Start a transaction
            with self.db_manager_psql.transaction():
                try:
                    # Add to the checksum table
                    self.update_checksum_in_db(file_url, new_checksum)

                    # Add to category (if not exists)
                    category_name = file_path.split('/')[1]
                    category_id = self.get_or_create_category(category_name)

                    # Add to documents table
                    document_id = self.insert_document(file_url, file_path, category_id)

                    # Add to embeddings (placeholder)
                    self.add_embedding(document_id)

                    # Add to S3
                    self.upload_to_s3(response.body, file_path)

                    # Commit the transaction
                    self.db_manager_psql.commit()
                    self.db_manager_sqlite.commit()

                except Exception as e:
                    # Roll back the transaction if an exception occurs
                    self.db_manager_psql.rollback()
                    raise e

        except Exception as e:
            error_message = f"Failed to process {file_path} due to {e}"
            self.logger.error(error_message)
            self.error_log.append(error_message)

    def get_or_create_category(self, category_name):
        result = self.db_manager_psql.execute(
            'SELECT id FROM categories WHERE name = :name',
            {'name': category_name}
        ).fetchone()
        if result:
            return result[0]
        else:
            self.db_manager_psql.execute(
                'INSERT INTO categories (name) VALUES (:name)',
                {'name': category_name}
            )
            return self.db_manager_psql.execute('SELECT lastval()').fetchone()[0]

    def insert_document(self, file_url, file_path, category_id):
        document_id = str(uuid.uuid4())
        self.db_manager_psql.execute(
            '''
            INSERT INTO documents (id, file_url, file_s3_path, category_id)
            VALUES (:id, :file_url, :file_path, :category_id)
            ''',
            {
                'id': document_id,
                'file_url': file_url,
                'file_path': file_path,
                'category_id': category_id
            }
        )
        return document_id

    def add_embedding(self, document_id):
        # Placeholder for adding embeddings
        pass

    def get_checksum_from_db(self, file_url):
        result = self.db_manager_sqlite.execute(
            'SELECT checksum FROM documents_checksums WHERE file_url = :file_url',
            {'file_url': file_url}
        ).fetchone()
        if result:
            self.update_last_accessed(file_url)  # Update last_accessed timestamp
        return result[0] if result else None

    def update_checksum_in_db(self, file_url, checksum):
        self.db_manager_sqlite.execute(
            '''
            INSERT INTO documents_checksums (id, checksum, file_url, created_at, updated_at)
            VALUES (:id, :checksum, :file_url, :created_at, :updated_at)
            ON CONFLICT(file_url) DO UPDATE SET checksum = :checksum, updated_at = :updated_at
            ''',
            {
                'id': str(uuid.uuid4()),
                'checksum': checksum,
                'file_url': file_url,
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            }
        )
        

    def update_last_accessed(self, file_url):
        self.db_manager_sqlite.execute(
            'UPDATE documents_checksums SET last_accessed = :last_accessed WHERE file_url = :file_url',
            {'last_accessed': datetime.now(), 'file_url': file_url}
        )
        self.db_manager_sqlite.commit()

    def upload_to_s3(self, file_content, file_path):
        upload_response = self.s3_client.put_object(Body=file_content, Bucket=self.bucket_name, Key=file_path)
        self.logger.info(f"S3 Upload Successful: {upload_response}")

    def closed(self, reason):
        self.db_manager_sqlite.close()
        if self.error_log:
            subject = "FCA Handbook Spider Error Report"
            message = "\n".join(self.error_log)
            send_email_alert(subject, message)