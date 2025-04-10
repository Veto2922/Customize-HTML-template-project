from src.llm_blocks_helper.api_key_loader import APIKeyLoader
from src.llm_blocks_helper.model_loader import ModelLoader
from src.llm_blocks_helper.prompt_loader import PromptLoader
from src.llm_blocks_helper.chain_builder import ChainBuilder
from src.Log_Manager.log_manager import get_logger
from src.schemas.custom_json_output_format import custom_json_output_parser

from .base import LLMProcessor
from src.llm_blocks_helper.base import BaseLLMComponent

logger = get_logger(__name__)

class CustomizeJsonPlaceholder(LLMProcessor):
    def __init__(self, api_key_loader: BaseLLMComponent, model_loader: BaseLLMComponent, 
                              prompt_loader: BaseLLMComponent, chain_builder: BaseLLMComponent):
        
        # Dependencies are injected through the constructor
        self.api_key_loader = api_key_loader
        self.model_loader = model_loader
        self.prompt_loader = prompt_loader
        self.chain_builder = chain_builder

    def run(self, business_name: str, business_description: str, images_description : dict ,json_placeholder: dict) -> dict:
        try:
            api_key = self.api_key_loader.execute()
            llm = self.model_loader.execute(api_key)
            prompt_template = self.prompt_loader.execute()
            chain = self.chain_builder.execute(prompt_template, llm, custom_json_output_parser)

            response = chain.invoke({
                "images_description" : images_description, 
                'json_placeholder': json_placeholder,
                'business_name': business_name,
                'business_description': business_description
            })

            logger.info("Response received successfully.")
            return response['updated_json_placeholder']

        except Exception as e:
            logger.exception("Error running chain: %s", e)
            raise