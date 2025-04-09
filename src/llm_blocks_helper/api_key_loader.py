import os
from dotenv import load_dotenv
from src.Log_Manager.log_manager import get_logger
from .base import BaseLLMComponent

logger = get_logger(__name__)

class APIKeyLoader(BaseLLMComponent):
    def __init__(self, env_var_name="GEMINI_API_KEY"):
        self.env_var_name = env_var_name

    def execute(self):
        try:
            load_dotenv()
            api_key = os.getenv(self.env_var_name)
            if not api_key:
                raise ValueError(f"API key not found in environment variable: {self.env_var_name}")
            logger.info("API key loaded successfully.")
            return api_key
        except Exception as e:
            logger.exception("Error loading API key: %s", e)
            raise