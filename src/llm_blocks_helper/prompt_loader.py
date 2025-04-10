from src.Log_Manager.log_manager import get_logger
from .base import BaseLLMComponent

logger = get_logger(__name__)

class PromptLoader(BaseLLMComponent):
    def __init__(self):
        pass

    def execute(self , prompt_file_path : str ):
        try:
            with open( prompt_file_path, 'r', encoding='utf-8') as file:
                prompt = file.read()
            logger.info("Prompt loaded from %s", prompt_file_path)
            return prompt
        except FileNotFoundError:
            logger.exception("Prompt file not found at %s", prompt_file_path)
            raise
        except Exception as e:
            logger.exception("Error loading prompt: %s", e)
            raise