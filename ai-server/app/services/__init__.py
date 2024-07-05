from ..config import BaseConfig

from qdrant_client import QdrantClient
qdrant_client = QdrantClient(url=BaseConfig.QDRANT_URL, api_key=BaseConfig.QDRANT_API_KEY)

import cohere
co = cohere.Client(api_key=BaseConfig.COHERE_API_KEY)

from .qdrant_retriever import QdrantRetriever
from .financial_regulation_query_handler import FinancialRegulationQueryHandler
from .query_decomposition import QueryDecomposition
from .financial_regulation_query_classifier import FinancialRegulationQueryClassifier


