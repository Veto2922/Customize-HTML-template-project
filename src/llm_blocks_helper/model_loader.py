from langchain_google_genai import ChatGoogleGenerativeAI
from src.Log_Manager.log_manager import get_logger
from .base import BaseLLMComponent

logger = get_logger(__name__)

class ModelLoader(BaseLLMComponent):
    def __init__(self, model_name="gemini-2.0-flash"):
        self.model_name = model_name

    def execute(self, api_key):
        try:
            llm = ChatGoogleGenerativeAI(model=self.model_name, google_api_key=api_key)
            logger.info("Model loaded successfully.")
            return llm
        except Exception as e:
            logger.exception("Failed to load model: %s", e)
            raise