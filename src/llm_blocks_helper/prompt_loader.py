from src.Log_Manager.log_manager import get_logger
from .base import BaseLLMComponent

logger = get_logger(__name__)

class PromptLoader(BaseLLMComponent):
    def __init__(self, prompt_file_path="prompts/customize_json_data_prompt.txt"):
        self.prompt_file_path = prompt_file_path

    def execute(self):
        try:
            with open(self.prompt_file_path, 'r', encoding='utf-8') as file:
                prompt = file.read()
            logger.info("Prompt loaded from %s", self.prompt_file_path)
            return prompt
        except FileNotFoundError:
            logger.exception("Prompt file not found at %s", self.prompt_file_path)
            raise
        except Exception as e:
            logger.exception("Error loading prompt: %s", e)
            raise