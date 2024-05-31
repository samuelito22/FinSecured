from sqlalchemy.orm import Session
from regulatory_scraper.database.models import Document
from sqlalchemy.sql import func
import uuid

class DocumentService:
    def __init__(self, session: Session):
        self.session = session

    def add_document(self, file_url, file_s3_path, category_id):
        """
        Add a new document entry to the database. 
        Parameters:
            file_url (str): URL of the file
            file_s3_path (str): Path where the file is stored on S3
            category_id (int): ID of the category the document belongs to
        """
        # First, check if the document already exists to avoid duplication
        existing_document = self.session.query(Document).filter_by(file_url=file_url).first()
        if existing_document:
            raise ValueError("A document with this file URL already exists.")

        # Create a new Document object with all required fields
        new_document = Document(
            file_url=file_url,
            file_s3_path=file_s3_path,
            category_id=category_id
        )
        self.session.add(new_document)
        return new_document
