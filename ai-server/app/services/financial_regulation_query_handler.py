from fastapi import HTTPException, status
from langchain_openai import ChatOpenAI
from typing import List, Dict
from llama_index.core.schema import Node
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from llama_index.core.schema import Node

class Citation(BaseModel):
    source_id: str = Field(
        description="The string ID of a SPECIFIC source which justifies the answer.",
    )
    quotes: List[str] = Field(
        description="All the VERBATIM quotes from the specified source that justifies the answer.",
    )

class QuotedAnswer(BaseModel):
    """Answer the user question based only on the given sources, and cite the sources used. Each fact in the answer should be supported by inline citations placed immediately after the statement. If multiple sources support the same fact, citations should be stacked. Ensure all relevant sources are utilized to construct a comprehensive answer."""
    answer: str = Field(
        description="The answer to the user question, formatted in a single, in-depth paragraph of 150 words, including inline citations in the format [Source ID].",
    )
    citations: List[Citation] = Field(
        description="The string IDs of the SPECIFIC sources which justify the answer and are cited inline using the modified IEEE style with square brackets.",
    )
    completed: bool = Field(
        description="True if the context was sufficient for a reliable response, False otherwise.",
    )

class FinancialRegulationQueryHandler:
    def __init__(self, model_name:str = "gpt-4o"):
        try:
            self.llm = ChatOpenAI(model=model_name, temperature=0)
            self.structured_llm = self.llm.with_structured_output(QuotedAnswer)
            self.prompt = self.setup_prompt()
        except Exception as e:
            # Handle initialization errors, possibly due to model availability or configuration issues
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                                detail=f"Failed to initialize AI model: {str(e)}")

    def setup_prompt(self):
        return ChatPromptTemplate.from_messages(
            [
                (
                    "system", system_prompt
                    
                ),
                ("human", "{query}")
            ]
        )

    async def handle_query(self, nodes, query):
        formatted_context = self.format_nodes_with_id(nodes)
        query_analyzer = self.prompt | self.structured_llm
        
        response = await query_analyzer.ainvoke({"query": query, "context": formatted_context, "example": example})
        
        quoted_answer = response.dict()
        citations = quoted_answer['citations']

        formatted_citations = []
        formatted_answer = quoted_answer['answer']

        for i, cit in enumerate(citations):
            file_url = next((node.metadata['file_url'] for node in nodes if node.metadata['document_id'] == cit['source_id']), None)

            temp = {
                "id": i + 1,
                "quotes": cit['quotes'],
                "document_id": cit['source_id'],
                "file_url": file_url
                }

            formatted_citations.append(temp)
            formatted_answer = formatted_answer.replace(cit['source_id'], str(temp['id']))

        return { 
            "answer": formatted_answer, 
            "completed": quoted_answer['completed'],
            "citations": formatted_citations
        }


    
    @staticmethod
    def format_nodes_with_id(nodes: List[Node]) -> str:
        formatted = [
            f"Source ID: {node.metadata['document_id']}\nDocument Snippet: {node.get_content()}"
            for node in nodes
        ]
        return "\n\n" + "\n\n".join(formatted)

system_prompt = (
    "As an expert in financial regulations, your task is to provide a single, in-depth paragraph "
    "that concisely and precisely answers the query. Include inline citations directly in your response "
    "by referencing source IDs in square brackets (e.g., [Source ID]) whenever you use information from the documents provided. "
    "For each citation, you must list all applicable verbatim quotes that justify your statements. "
    "If multiple sources support the same fact, stack the citations immediately after the statement. "
    "Ensure that you utilize all relevant sources to provide a comprehensive answer. If the context provided is insufficient for "
    "a reliable response, explicitly inform the user that a complete and accurate answer cannot be generated due to this limitation. "
    "Each citation must comprehensively cover all the statements it supports with as many quotes as necessary to fully justify the answer given.\n\n"
    "Example:\n{example}\n\n"
    "Context for answering the query:\n{context}"
)


example = """
The term 'Basel IV' might refer to the most recent amendment of the Basel Accords by the Basel Committee on Banking Supervision, which mandates more stringent capital requirements and risk management procedures for banks worldwide [d83452fa-8b7c-499a-b1c8-1d1d84c6ad2f].
Additionally, Dr. Maria Lopez from the University of Madrid has contributed to research on the impact of these regulations on small to medium-sized enterprises (SMEs),
particularly in how they access credit in a tighter regulatory environment, indicating a potential need for policy adjustments [d2f51936-c4eb-4e9c-aa8c-d1b2e8ad2f91][e1a2d39b-4423-4f18-9923-c4c8d5b9c8e2].
Furthermore, Professor John Cartwright's analysis on liquidity requirements under Basel IV emphasizes the increased safety net for banks but also points out the pressure it puts on banks' operational flexibility, especially under economic stress [a7c1d3e2-4a8e-4b5a-9941-8b21b9f35d3c].
Thus, 'Basel IV' could potentially enhance the stability of the financial system globally by incorporating rigorous standards, advanced risk assessment methodologies, and increased transparency, while also possibly restricting the economic activities of banks in certain aspects.
"""