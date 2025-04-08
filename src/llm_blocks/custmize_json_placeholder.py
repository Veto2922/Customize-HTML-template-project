# customize_json_processor.py
import os
import logging
from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from .base import LLMProcessor
from src.schemas.custom_json_output_format import custom_json_output_parser
from src.Log_Manager.log_manager import get_logger


# Setup logging
logger = get_logger(__name__)

class CustomizeJsonPlaceholder(LLMProcessor):
    def __init__(self):
        try:
            load_dotenv()
            self.api_key = os.getenv("GEMINI_API_KEY")
            if not self.api_key:
                raise ValueError("API key not found in environment variable: GEMINI_API_KEY")
            logger.info("API key loaded successfully.")
        except Exception as e:
            logger.exception("Error during initialization: %s", e)
            raise

    def load_model(self):
        try:
            self.llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=self.api_key)
            logger.info("Model loaded successfully.")
        except Exception as e:
            logger.exception("Failed to load model: %s", e)
            raise

    def load_prompt(self):
        try:
            prompt_path = os.path.join('prompts', 'customize_json_data_prompt.txt')
            with open(prompt_path, 'r', encoding='utf-8') as file:
                self.customize_json_data_prompt = file.read()
            logger.info("Prompt loaded from %s", prompt_path)
        except FileNotFoundError:
            logger.exception("Prompt file not found at %s", prompt_path)
            raise
        except Exception as e:
            logger.exception("Error loading prompt: %s", e)
            raise

    def build_chain(self):
        try:
            prompt = PromptTemplate(
                template=self.customize_json_data_prompt,
                partial_variables={"format_instructions": custom_json_output_parser.get_format_instructions()}
            )
            self.chain = prompt | self.llm | custom_json_output_parser
            logger.info("LLM chain built successfully.")
        except Exception as e:
            logger.exception("Error building chain: %s", e)
            raise

    def run(self, business_name: str, business_description: str, json_placeholder: str):
        try:
            self.load_model()
            self.load_prompt()
            self.build_chain()

            if not self.chain:
                raise ValueError("Chain is not built. Call build_chain() first.")

            logger.info("Running chain with business_name='%s'", business_name)

            response = self.chain.invoke({
                'json_placeholder': json_placeholder,
                'business_name': business_name,
                'business_description': business_description
            })

            logger.info("Response received successfully.")
            return response['updated_json_placeholder']

        except Exception as e:
            logger.exception("Error running chain: %s", e)
            raise

if __name__ == "__main__":
    try:
        processor = CustomizeJsonPlaceholder()
        result = processor.run(
            business_name="My Business",
            business_description="A description of my business",
            json_placeholder='{"business name": "value"}'
        )
        print(result)
    except Exception as e:
        logger.critical("Application crashed: %s", e)
