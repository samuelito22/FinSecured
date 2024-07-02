from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import asyncio
import itertools
from typing import List, Dict

from ...services import QdrantRetriever, QueryDecomposition, FinancialRegulationQueryHandler, FinancialRegulationQueryClassifier
from ...common.config import BaseConfig 
from ..utils.auth import require_secret_key

router = APIRouter(prefix="/documents", tags=["documents"], responses={404: {"description": "Not found"}})

class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=1024, description="The query to process")
    regulation: str = Field(..., pattern="^(FCA)$", description="The regulation applicable")

@router.post("/answer", summary="Process and answer the query based on the regulations", status_code=status.HTTP_200_OK)
async def answer_query(request_data: QueryRequest, token: str = Depends(require_secret_key)):
    try:
        _query = request_data.query
        _regulation = request_data.regulation

        classifier = FinancialRegulationQueryClassifier(model_name="gpt-3.5-turbo-0125")
        query_needs_context = await classifier.classify(_query)

        if not query_needs_context:
            return JSONResponse(content={"success": True, "message": "This query does not require specific regulatory context." ,"data": {"answer": "This query does not require specific regulatory context.", "complted": False, "citations": []}})

        query_decomposition = QueryDecomposition(model_name="gpt-3.5-turbo-0125")
        subquery_results = await query_decomposition.decompose(_query)

        qdrant_retriever = QdrantRetriever(collection_name=f"{_regulation.lower()}_regulatory")
        retrieve_tasks = [qdrant_retriever.retrieve_nodes(sq['sub_query']) for sq in subquery_results]
        context = await asyncio.gather(*retrieve_tasks)

        query_handler = FinancialRegulationQueryHandler(model_name="gpt-4o-2024-05-13")
        response = await query_handler.handle_query(list(itertools.chain.from_iterable(con['results'] for con in context)), _query)

        return JSONResponse(content={
            "success": True, 
            "message": "Query processed successfully.",
            "data": response
        })
    except HTTPException as http_exc:
        return JSONResponse(content={"success": False, "message": str(http_exc.detail)}, status_code=http_exc.status_code)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

