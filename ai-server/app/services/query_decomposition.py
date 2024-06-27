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

class QueryDecomposition():
    def __init__(self, model_name: str = "gpt-3.5-turbo-0125"):
        self.llm = ChatOpenAI(model=model_name, temperature=0)

    async def decompose(self, query: str) -> List[Dict[str, str]]:
        llm = self.llm
        prompt = ChatPromptTemplate.from_messages([("system", system), ("human", "{query}")])
        llm_with_tools = llm.bind_tools([SubQuery])
        parser = PydanticToolsParser(tools=[SubQuery])
        query_analyzer = prompt | llm_with_tools | parser
        
        response = await query_analyzer.ainvoke({"query": query})

        return [res.dict() for res in response]

system = """You are an expert at converting user questions into detailed sub-queries for a financial regulations database.
  You have access to a comprehensive database of financial regulations, amendments, and historical changes.
  Perform query decomposition. Given a user question, break it down into distinct sub-questions that
  you need to answer to provide a thorough response.
  If there are acronyms or technical terms, clarify them within the sub-queries.
  If the query is already precise and detailed, proceed with it as is. """
