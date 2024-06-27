from qdrant_client import QdrantClient
from typing import Dict, List
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import VectorStoreIndex
from llama_index.core.schema import Node
from . import co, embed_model
from . import qdrant_client

class QdrantRetriever:
    def __init__(self, collection_name: str, qdrant_client: QdrantClient = qdrant_client):
        self.qdrant_client = qdrant_client
        self.vector_store = QdrantVectorStore(collection_name, qdrant_client, enable_hybrid=True)

    async def retrieve_nodes(self, query: str) -> Dict[str, List[Node]]:
        index_retriever = VectorStoreIndex.from_vector_store(self.vector_store, embed_model).as_retriever(similarity_top_k=10, sparse_top_k=20, vector_store_query_mode="hybrid")

        results = index_retriever.retrieve(query)
        reranked_results = co.rerank(model="rerank-english-v3.0", query=query, documents=[node.get_content() for node in results], top_n=4)
        top_indices = [result.index for result in reranked_results.results]
        top_results = [results[i] for i in top_indices]

        return {'query': query, 'results': top_results}
