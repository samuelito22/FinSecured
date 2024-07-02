from fastapi import HTTPException, status
from langchain_openai import ChatOpenAI
from typing import Dict, List
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.output_parsers import PydanticToolsParser
from langchain_core.prompts import ChatPromptTemplate

class SubQuery(BaseModel):
    """Search over a database of detailed documents on financial regulations."""
    sub_query: str = Field(
        description="A very specific query related to financial regulations."
    )

class QueryDecomposition:
    def __init__(self, model_name: str = "gpt-3.5-turbo-0125"):
        try:
            self.llm = ChatOpenAI(model=model_name, temperature=0)
        except Exception as e:
            # Handle initialization errors, such as connection issues or incorrect model names
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                                detail=f"Failed to initialize AI model: {str(e)}")

    async def decompose(self, query: str) -> List[Dict[str, str]]:
        try:
            prompt = ChatPromptTemplate.from_messages([
                ("system", system),
                ("human", "{query}")
            ])
            llm_with_tools = self.llm.bind_tools([SubQuery])
            parser = PydanticToolsParser(tools=[SubQuery])
            query_analyzer = prompt | llm_with_tools | parser
            
            response = await query_analyzer.ainvoke({"query": query})
            return [res.dict() for res in response]
        except Exception as e:
            # General exception for errors during decomposition or API calls
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Error during query decomposition: {str(e)}")

system = """You are an expert at converting user questions into detailed sub-queries for a financial regulations database.
  You have access to a comprehensive database of financial regulations, amendments, and historical changes.
  Perform query decomposition. Given a user question, break it down into distinct sub-questions that
  you need to answer to provide a thorough response.
  If there are acronyms or technical terms, clarify them within the sub-queries.
  If the query is already precise and detailed, proceed with it as is. """
