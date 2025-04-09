from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from src.Log_Manager.log_manager import get_logger
from .base import BaseLLMComponent

logger = get_logger(__name__)

class ChainBuilder(BaseLLMComponent):
    def execute(self, prompt_template, llm, output_parser):
        try:
            prompt = PromptTemplate(
                template=prompt_template,
                partial_variables={"format_instructions": output_parser.get_format_instructions()}
            )
            chain = prompt | llm | output_parser
            logger.info("LLM chain built successfully.")
            return chain
        except Exception as e:
            logger.exception("Error building chain: %s", e)
            raise