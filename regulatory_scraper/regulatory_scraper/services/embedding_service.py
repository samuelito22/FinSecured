import os
import re
import fitz  # PyMuPDF
from io import BytesIO
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_postgres.vectorstores import PGVector
from langchain.schema import Document  # Import Document schema
from regulatory_scraper.config import PGVECTOR_CONNECTION

class EmbeddingService:
    def __init__(self):
        # Initialize components
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=80)
        self.embeddings = HuggingFaceEmbeddings()
        self.document = None
        self.chunks = []

        
        self.pg_vector_store = PGVector(
            embeddings=self.embeddings,
            connection=PGVECTOR_CONNECTION,
            collection_name="embeddings",
        )
        

    def load_pdf_document(self, pdf_body):
        """Loads a PDF and stores the content into self.document."""
        try:
            text = self.extract_text_with_pymupdf(pdf_body)
            self.document = Document(page_content=text)
        except Exception as e:
            raise ValueError(f"Failed to load PDF document: {str(e)}")

    def extract_text_with_pymupdf(self, pdf_body):
        """Extracts text from a PDF using PyMuPDF (fitz)."""
        # Create a BytesIO stream from the PDF body
        doc = fitz.open("pdf", pdf_body)
        text = ""
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text += page.get_text()
        doc.close()  # Ensure the document is closed after extracting text
        return text

    def split_into_chunks(self):
        """Splits loaded document into chunks."""
        if not self.document:
            raise ValueError("Document is not loaded. Please load a document before splitting.")
        self.chunks = self.text_splitter.split_documents([self.document])

    def clean_text(self, text):
        # Remove \n and replace \xa0 with space
        cleaned_text = text.replace('\n', ' ').replace('\xa0', ' ')
        # Remove extra spaces
        cleaned_text = re.sub(' +', ' ', cleaned_text)
        return cleaned_text

    def vectorize_and_store_embeddings(self, document_id):
        """Vectorizes the text chunks and stores them as embeddings."""
        if not self.chunks:
            raise ValueError("No chunks to process. Please split a document before vectorizing.")
        chunk_contents = [self.clean_text(chunk.page_content) for chunk in self.chunks]

        embeddings = self.embeddings.embed_documents([chunk.page_content for chunk in self.chunks])

        # Convert document_id to string if it's a UUID
        document_id_str = str(document_id)

        # Create metadata for each chunk. For simplicity, storing the document ID and the index of the chunk.
        metadatas = [{'document_id': document_id_str, 'chunk_index': idx} for idx, _ in enumerate(chunk_contents)]

        # Generate unique IDs for each chunk.
        chunk_ids = [f"{document_id_str}-{idx}" for idx in range(len(chunk_contents))]

        # Store the embeddings in the vector store.
        stored_ids = self.pg_vector_store.add_embeddings(texts=chunk_contents, embeddings=embeddings, metadatas=metadatas, ids=chunk_ids)

        return stored_ids


    def clear(self):
        self.document = None
        self.chunks = []

    def process_and_store_document_embeddings(self, pdf_body, document_id):
        self.load_pdf_document(pdf_body)
        self.split_into_chunks()
        store_ids = self.vectorize_and_store_embeddings(document_id)

        self.clear()

        return store_ids
