from fastapi import HTTPException, status
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
        try:
            self.llm = ChatOpenAI(temperature=0.5, model=model_name).with_structured_output(QueryNeedsContext)
            self.decision_chain = prompt_template | self.llm
        except Exception as e:
            # Handle initialization errors, such as connection issues or incorrect model names
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                                detail=f"Failed to initialize AI model: {str(e)}")

    async def classify(self, query: str) -> bool:
        """Determine if the provided financial regulation query needs additional context."""
        try:
            response = await self.decision_chain.ainvoke({'input': query})
            return response.dict()['needs_context']
        except ValueError as ve:
            # This could happen if the response format is unexpected or misconfigured
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail=f"Response parsing error: {str(ve)}")
        except Exception as e:
            # Generic exception for other unforeseen errors
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"An error occurred during query classification: {str(e)}")

