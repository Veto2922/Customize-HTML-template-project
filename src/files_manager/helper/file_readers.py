
import json
from src.files_manager.helper.base import FileReader

from src.Log_Manager.log_manager import get_logger

logger = get_logger(__name__)

class JsonFileReader(FileReader):
    """Concrete implementation for reading JSON files"""
    def read(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as file:
                content = json.load(file)
            logger.info("JSON content loaded from: %s", path)
            return content
        except FileNotFoundError:
            logger.error("JSON file not found at path: %s", path)
            raise
        except json.JSONDecodeError:
            logger.error("Failed to decode JSON from: %s", path)
            raise
        except Exception as e:
            logger.exception("Unexpected error loading JSON content.")
            raise

class TextFileReader(FileReader):
    """Concrete implementation for reading text/HTML files"""
    def read(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
            logger.info("Text content loaded from: %s", path)
            return content
        except FileNotFoundError:
            logger.error("Text file not found at path: %s", path)
            raise
        except Exception as e:
            logger.exception("Unexpected error loading text content.")
            raise