from langchain_core.prompts import PromptTemplate
from src.schemas.episode import SemanticFacts
from .prompts import FACT_EXTRACTION_PROMPT_STR
# Chat model
from langchain_core.language_models.chat_models import BaseChatModel
from typing import List

class FactParser:
    @staticmethod
    async def parse(llm: BaseChatModel,
                    contents: List[str]) -> List[SemanticFacts]:
        """
        Parse text contents to extract semantic facts using LLM.
        
        Args:
            llm: The language model to use for fact extraction
            contents: List of text contents to parse for semantic facts
            
        Returns:
            List[SemanticFacts]: List of extracted semantic facts for each content
            
        Raises:
            Exception: If LLM processing fails
        """
        FACT_EXTRACTION_PROMPT = PromptTemplate(
            input_variables=["text"],
            template = FACT_EXTRACTION_PROMPT_STR,
        )

        structured_llm = llm.with_structured_output(SemanticFacts)

        # Using invoke or batch based on number of elements
        if len(contents) == 1:
            # Invoke case
            prompt = FACT_EXTRACTION_PROMPT.format(text = contents[0])
            return [await structured_llm.ainvoke(prompt)]
        else:
            # Batch case - apply prompt template then batch
            formatted_prompts = [FACT_EXTRACTION_PROMPT.format(text = content) for content in contents]
            return await structured_llm.abatch(formatted_prompts)

