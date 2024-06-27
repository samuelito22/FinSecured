from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field

class QueryNeedsContext(BaseModel):
    needs_context: bool = Field(description="True if the query needs context retrieval, False otherwise")

prompt_template = ChatPromptTemplate.from_template(
    """
    Analyze if the following query about financial regulations needs additional context from a database for an accurate response.
    Consider queries needing detailed examples, historical data, or specific regulatory nuances as requiring context.

    Query:
    {input}

    Response (True or False):
    """
)

class FinancialRegulationQueryClassifier:
    def __init__(self, model_name: str = "gpt-3.5-turbo-0125"):
        llm = ChatOpenAI(temperature=0.5, model="gpt-3.5-turbo-0125").with_structured_output(QueryNeedsContext)
        self.decision_chain = prompt_template | llm

    async def classify(self, query: str) -> bool:
        """Determine if the provided financial regulation query needs additional context."""
        response = await self.decision_chain.ainvoke({'input':query})
        return response.dict()['needs_context']