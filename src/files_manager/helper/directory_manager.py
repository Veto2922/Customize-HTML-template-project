
import os
from src.Log_Manager.log_manager import get_logger
from src.files_manager.helper.base import DirectoryManager

logger = get_logger(__name__)

class FileSystemDirectoryManager(DirectoryManager):
    """Concrete implementation for directory operations"""
    def ensure_directory_exists(self, directory_path):
        try:
            if not os.path.exists(directory_path):
                os.makedirs(directory_path)
                logger.info("Created directory: %s", directory_path)
            return True
        except PermissionError:
            logger.error("Permission denied when creating directory: %s", directory_path)
            raise
        except Exception as e:
            logger.exception("Failed to create directory: %s", directory_path)
            raise
    
    def list_files_with_extensions(self, directory_path, extensions):
        try:
            if not os.path.exists(directory_path):
                logger.error("Directory does not exist: %s", directory_path)
                raise FileNotFoundError(f"Directory does not exist: {directory_path}")
                
            files = [f for f in os.listdir(directory_path) 
                    if os.path.isfile(os.path.join(directory_path, f)) and 
                    os.path.splitext(f)[1].lower() in extensions]
            
            logger.info("Found %d files with specified extensions in %s", len(files), directory_path)
            return files
        except Exception as e:
            logger.exception("Error listing files in directory: %s", directory_path)
            raise