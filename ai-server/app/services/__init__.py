from ..common.config import BaseConfig

from qdrant_client import QdrantClient
qdrant_client = QdrantClient(host="localhost", port=6333)

from llama_index.embeddings.huggingface import HuggingFaceEmbedding
embed_model = HuggingFaceEmbedding(model_name="thenlper/gte-large")

import cohere
co = cohere.Client(api_key=BaseConfig.COHERE_API_KEY)

from .qdrant_retriever import QdrantRetriever
from .financial_regulation_query_handler import FinancialRegulationQueryHandler
from .query_decomposition import QueryDecomposition
from .financial_regulation_query_classifier import FinancialRegulationQueryClassifier


