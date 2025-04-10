
import shutil
from src.files_manager.helper.base import FileCopier

from src.Log_Manager.log_manager import get_logger

logger = get_logger(__name__)

class FileSystemCopier(FileCopier):
    """Concrete implementation for copying files"""
    def copy(self, source_path, destination_path):
        try:
            shutil.copy2(source_path, destination_path)
            logger.info("Copied file from %s to %s", source_path, destination_path)
        except FileNotFoundError:
            logger.error("Source file not found: %s", source_path)
            raise
        except PermissionError:
            logger.error("Permission denied when copying file from %s to %s", source_path, destination_path)
            raise
        except Exception as e:
            logger.exception("Failed to copy file from %s to %s", source_path, destination_path)
            raise