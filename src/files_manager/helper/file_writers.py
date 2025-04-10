from src.files_manager.helper.base import FileWriter
from src.Log_Manager.log_manager import get_logger

logger = get_logger(__name__)

class TextFileWriter(FileWriter):
    """Concrete implementation for writing text/HTML files"""
    def write(self, content, path):
        try:
            with open(path, 'w', encoding='utf-8') as file:
                file.write(content)
            logger.info("Content saved to: %s", path)
        except Exception as e:
            logger.exception("Failed to save content to %s", path)
            raise