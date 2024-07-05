from fastapi import HTTPException, status
from qdrant_client import QdrantClient
from typing import Dict, List
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import VectorStoreIndex
from llama_index.core.schema import Node
from . import co
from . import qdrant_client

class QdrantRetriever:
    def __init__(self, collection_name: str, qdrant_client: QdrantClient = qdrant_client):
        # Import embed_model inside the class
        from .. import embed_model

        if embed_model is None:
            raise HTTPException(status_code=503, detail="Model is not loaded yet, try again later.")
        
        self.embed_model = embed_model
        
        try:
            self.qdrant_client = qdrant_client
            self.vector_store = QdrantVectorStore(collection_name, qdrant_client, enable_hybrid=True)
        except Exception as e:
            # Initialization errors might occur if the connection to Qdrant fails or if the collection is not found
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                                detail=f"Failed to initialize Qdrant Vector Store: {str(e)}")

    async def retrieve_nodes(self, query: str) -> Dict[str, List[Node]]:
        try:
            # Use self.embed_model here
            index_retriever = VectorStoreIndex.from_vector_store(self.vector_store, self.embed_model).as_retriever(similarity_top_k=10, sparse_top_k=10, vector_store_query_mode="hybrid")
            results = index_retriever.retrieve(query)
            reranked_results = co.rerank(model="rerank-english-v3.0", query=query, documents=[node.get_content() for node in results], top_n=4)
            top_indices = [result.index for result in reranked_results.results]
            top_results = [results[i] for i in top_indices]

            if not top_results:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="No relevant results found for the given query.")

            return {'query': query, 'results': top_results}
        except Exception as e:
            # General exception for errors during retrieval or processing
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Error during node retrieval: {str(e)}")
