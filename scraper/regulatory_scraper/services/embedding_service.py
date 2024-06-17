import os
import re
import fitz  # PyMuPDF
from io import BytesIO
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_cohere import CohereEmbeddings
from langchain_postgres.vectorstores import PGVector
from langchain.schema import Document  # Import Document schema
from regulatory_scraper.config import PGVECTOR_CONNECTION
from regulatory_scraper.utils.processing import extract_text_with_pymupdf
import time


def rate_limited(max_per_minute):
    print("Initiating cooldown...")
    min_interval = 60.0 / float(max_per_minute)
    def decorate(func):
        last_time_called = [0.0]
        def rate_limited_function(*args, **kwargs):
            elapsed = time.time() - last_time_called[0]
            left_to_wait = min_interval - elapsed
            if left_to_wait > 0:
                time.sleep(left_to_wait)
            last_time_called[0] = time.time()
            return func(*args, **kwargs)
        return rate_limited_function
    return decorate

class EmbeddingService:
    def __init__(self, collection_name):
        # Initialize components
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=50)
        self.embeddings = CohereEmbeddings(model="embed-english-v3.0")
        self.embed_documents = rate_limited(5)(self.embeddings.embed_documents)
        self.collection_name = collection_name

        self.document = None
        self.chunks = []

        
        self.pg_vector_store = PGVector(
            embeddings=self.embeddings,
            connection=PGVECTOR_CONNECTION,
            collection_name=collection_name,
        )
        

    def load_pdf_document(self, pdf_body):
        """Loads a PDF and stores the content into self.document."""
        try:
            text = extract_text_with_pymupdf(pdf_body)
            self.document = Document(page_content=text)
        except Exception as e:
            raise ValueError(f"Failed to load PDF document: {str(e)}")

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

    def vectorize_and_store_embeddings(self, document_id, keywords, jurisdiction):
        if not self.chunks:
            raise ValueError("No chunks to process. Please split a document before vectorizing.")

        # Prepare text chunks and clean them
        chunk_contents = [self.clean_text(chunk.page_content) for chunk in self.chunks]

        # Batch processing
        max_batch_size = 96
        stored_ids = []
        for i in range(0, len(chunk_contents), max_batch_size):
            batch_chunks = chunk_contents[i:i + max_batch_size]
            embeddings = self.embed_documents(batch_chunks)

            # Metadata for each chunk
            metadatas = [
                {'document_id': str(document_id), 'keywords': keywords, 'regulation_body': self.collection_name,
                'jurisdiction': jurisdiction, 'chunk_index': idx + i}
                for idx in range(len(batch_chunks))
            ]

            # Unique IDs for each chunk
            chunk_ids = [f"{str(document_id)}-{idx + i}" for idx in range(len(batch_chunks))]

            # Store the embeddings
            stored_batch_ids = self.pg_vector_store.add_embeddings(texts=batch_chunks, embeddings=embeddings, metadatas=metadatas, ids=chunk_ids)
            stored_ids.extend(stored_batch_ids)

        return stored_ids



    def clear(self):
        self.document = None
        self.chunks = []

    def process_and_store_document_embeddings(self, pdf_body, document_id, keywords, jurisdiction):
        self.load_pdf_document(pdf_body)
        self.split_into_chunks()
        store_ids = self.vectorize_and_store_embeddings(document_id, keywords, jurisdiction)

        self.clear()

        return store_ids

    def delete_document_embeddings(self, document_id):
        """
        Deletes all embeddings for a specific document ID.
        Parameters:
            document_id (str or UUID): The unique identifier for the document whose embeddings need to be deleted.
        Returns:
            int: The number of embeddings deleted.
        """
        # Convert document_id to string if it's a UUID
        document_id_str = str(document_id)
        
        # Delete embeddings where the 'document_id' in the metadata matches the provided document_id
        count_deleted = self.pg_vector_store.delete(metadata={'document_id': document_id_str})
        
        return count_deleted

    def delete_documents_embeddings(self, document_ids):
        document_ids_str = [str(document_id) for document_id in document_ids]
        num_deleted = self.pg_vector_store.delete({
            'metadata.document_id': {'$in': document_ids_str}
        })
        return num_deleted

