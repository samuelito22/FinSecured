# Standard library imports
import os
import re
import time
from io import BytesIO

# Third-party library imports
import fitz  # PyMuPDF
from sqlalchemy import make_url
import qdrant_client
from qdrant_client import models, QdrantClient

# Local application/library specific imports
from llama_index.core import VectorStoreIndex, Document
from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.qdrant import QdrantVectorStore
from regulatory_scraper.config import PGVECTOR_CONNECTION, QDRANT_URL
from regulatory_scraper.utils import extract_text_with_pymupdf, SafeSemanticSplitter

class EmbeddingService:
    def __init__(self, collection_name):
        self.collection_name = collection_name
        self.initialize_components()
        self.setup_qdrant()

    def initialize_components(self):
        self.embed_model = HuggingFaceEmbedding(model_name="thenlper/gte-large")
        self.splitter = SafeSemanticSplitter(
            buffer_size=1,
            breakpoint_percentile_threshold=80,
            embed_model=self.embed_model,
            safety_chunk_size=1024,
            safety_chunk_overlap=80
        )
        self.qdrant_client = QdrantClient(url=QDRANT_URL)
        self.vector_store = QdrantVectorStore(client=self.qdrant_client, collection_name=self.collection_name, enable_hybrid=True)
        self.vector_index = VectorStoreIndex.from_vector_store(self.vector_store, self.embed_model)

    def setup_qdrant(self):
        if not self.qdrant_client.collection_exists(collection_name=self.collection_name):
            self.qdrant_client.create_collection(
                self.collection_name,
                vectors_config={
                    "text-dense": models.VectorParams(
                    size=1024,
                    distance=models.Distance.COSINE,
                    on_disk=True,
                )
                },
                quantization_config=models.BinaryQuantization(
                    binary=models.BinaryQuantizationConfig(always_ram=True),
                ),
                sparse_vectors_config={
                    "text-sparse": models.SparseVectorParams(
                        index=models.SparseIndexParams(
                            on_disk=False,
                        )
                    )
                },
                
            )

    def process_document(self, pdf_body, document_id, regulation, file_url):
        self.document = self.load_pdf_document(pdf_body)
        self.nodes = self.split_into_nodes(self.document)
        self.vectorize_and_store_embeddings(document_id, regulation, file_url)
        self.clear()

    def load_pdf_document(self, pdf_body):
        try:
            text = extract_text_with_pymupdf(pdf_body)
            return Document(text=text)
        except Exception as e:
            raise ValueError(f"Failed to load PDF document: {str(e)}")

    def split_into_nodes(self, document):
        if not document:
            raise ValueError("Document is not loaded. Please load a document before splitting.")

        return self.splitter.get_nodes_from_documents([document])

    def vectorize_and_store_embeddings(self, document_id, regulation, file_url):
        if not self.nodes:
            raise ValueError("No node to process. Please split a document before vectorizing.")
        for node in self.nodes:
            node.set_content(node.get_content().replace('\n', " "))

            metadata = {
                'document_id': str(document_id),
                'regulation_body': regulation,
                'file_url': file_url
            }
            node.metadata = metadata

            embeddings = self.embed_model.get_text_embedding(
                node.get_content(metadata_mode="all")
            )

            node.embedding = embeddings
        self.vector_index.insert_nodes(self.nodes)

    def clear(self):
        self.document = None
        self.nodes = []

    def delete_document_embeddings(self, document_id):
        document_id_str = str(document_id)
        return self.vector_store.delete(metadata={'document_id': document_id_str})

    def delete_documents_embeddings(self, document_ids):
        document_ids_str = [str(document_id) for document_id in document_ids]
        return self.vector_store.delete({'metadata.document_id': {'$in': document_ids_str}})
