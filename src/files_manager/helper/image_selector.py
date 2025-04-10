
import random
from src.Log_Manager.log_manager import get_logger

logger = get_logger(__name__)

class ImageSelector:
    """Class responsible for selecting random images"""
    def __init__(self, directory_manager, file_copier):
        self.directory_manager = directory_manager
        self.file_copier = file_copier
        logger.info("ImageSelector initialized.")
    
    def select_random_image(self, image_folder, extensions):
        """Select a random image from a folder with specified extensions"""
        try:
            images = self.directory_manager.list_files_with_extensions(image_folder, extensions)
            if not images:
                logger.error("No images found in directory: %s", image_folder)
                raise ValueError(f"No images with specified extensions found in {image_folder}")
            
            selected_image = random.choice(images)
            logger.info("Randomly selected image: %s", selected_image)
            return selected_image
        except Exception as e:
            logger.exception("Error selecting random image.")
            raise