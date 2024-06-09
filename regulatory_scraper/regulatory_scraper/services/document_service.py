from sqlalchemy.orm import Session
from regulatory_scraper.database.models import Document
from sqlalchemy.sql import func
import uuid

class DocumentService:
    def add_document(self, session: Session, file_url, file_s3_path, category_id, regulation):
        """
        Add a new document entry to the database. 
        Parameters:
            file_url (str): URL of the file
            file_s3_path (str): Path where the file is stored on S3
            category_id (int): ID of the category the document belongs to
        """
        # First, check if the document already exists to avoid duplication
        existing_document = session.query(Document).filter_by(file_url=file_url).first()
        if existing_document:
            raise ValueError("A document with this file URL already exists.")

        # Create a new Document object with all required fields
        new_document = Document(
            file_url=file_url,
            file_s3_path=file_s3_path,
            category_id=category_id,
            regulation=regulation
        )
        session.add(new_document)
        return new_document

    def delete_document(self, session: Session, file_url):
        """
        Delete a document entry from the database based on its file URL and return the deleted document.
        Parameters:
            file_url (str): URL of the file to be deleted.
        Returns:
            Document: The deleted document object if found and deleted, None otherwise.
        """
        # Retrieve the document by URL
        document_to_delete = session.query(Document).filter_by(file_url=file_url).first()
        if document_to_delete:
            # Keep a copy of the document to return after deletion
            deleted_document = document_to_delete
            session.delete(document_to_delete)
            return deleted_document  # Return the deleted document object
        else:
            return None  

    def get_document_by_id(self, session: Session, document_id):
        """
        Retrieve a document entry from the database based on its document ID.
        Parameters:
            document_id (int or UUID): ID of the document to retrieve.
        Returns:
            Document: The document object if found, None otherwise.
        """
        document = session.query(Document).get(document_id)
        return document

    def get_document(self, session: Session, **filters):
        query = session.query(Document)
        for attribute, value in filters.items():
            query = query.filter(getattr(Document, attribute) == value)
        return query.first()

    def get_documents(self, session: Session, **filters):
        query = session.query(Document)
        for attribute, value in filters.items():
            query = query.filter(getattr(Document, attribute) == value)
        return query.all()
