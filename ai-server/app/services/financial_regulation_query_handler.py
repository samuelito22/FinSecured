from langchain_openai import ChatOpenAI
from typing import List, Dict
from llama_index.core.schema import Node
from langchain_core.prompts import ChatPromptTemplate

class FinancialRegulationQueryHandler:
    def __init__(self, model_name:str ="gpt-4o"):
        self.llm = ChatOpenAI(model=model_name, temperature=0)
        self.prompt_template = self.setup_prompt()

    def setup_prompt(self):
        return ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "As an expert in financial regulations, your task is to provide concise and precise answers. "
                    "You will handle user queries by considering each subquery within its specific context provided. "
                    "Should the context be insufficient for a reliable response, you are to explicitly inform the user "
                    "that a complete and accurate answer cannot be generated due to this limitation."
                    "\n This is the context provided to answer the query: \n {context} \n"
                ),
                ("human", "{query}")
            ]
        )

    async def handle_query(self, context: List[Dict[str, List[Node]]], query: str) -> str:
        chain = self.prompt_template | self.llm
        response = await chain.ainvoke({"context": self.format_context(context), "query": query})
        response_text = response.pretty_repr()
        return self.clean_response(response_text)
    
    @staticmethod
    def format_context(context: List[Dict[str, List[Node]]]):
        formatted_contexts = []
        for context_item in context:
            subquery = context_item['query']
            results = context_item['results']
            context_parts = [f"This is the context for the following subquery: {subquery}"]
            context_parts.extend([result.get_content() for result in results])
            formatted_context = "\n".join(context_parts)
            formatted_contexts.append(formatted_context)
        return "\n\n".join(formatted_contexts)

    @staticmethod
    def clean_response(response_text:str):
        return response_text.replace("================================== Ai Message ==================================\n\n", "")