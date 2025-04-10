import os
from src.Log_Manager.log_manager import get_logger

logger = get_logger(__name__)

class ImagePlaceholderProcessor:
    """Class responsible for processing image placeholders in HTML"""
    def __init__(self, image_selector, directory_manager):
        self.image_selector = image_selector
        self.directory_manager = directory_manager
        logger.info("ImagePlaceholderProcessor initialized.")
    
    def process_image_placeholders(self, html_template, image_placeholders, src_root_folder, dest_folder, image_extensions={'.jpg', '.jpeg', '.png', '.bmp', '.gif'}):
        """Process image placeholders in HTML template"""
        try:
            # Ensure destination folder exists
            self.directory_manager.ensure_directory_exists(dest_folder)
            
            result = html_template
            
            for key, value in image_placeholders.items():
                # Count occurrences of placeholder in template
                placeholder_count = result.count(key)
                
                # Get image folder path
                image_folder = os.path.join(src_root_folder, value['size'])
                
                # Process each occurrence of the placeholder
                for _ in range(placeholder_count):
                    # Select random image
                    selected_image = self.image_selector.select_random_image(image_folder, image_extensions)
                    selected_image_path = os.path.join(image_folder, selected_image)
                    
                    # Copy image to destination
                    dest_image_path = os.path.join(dest_folder, selected_image)
                    self.image_selector.file_copier.copy(selected_image_path, dest_image_path)
                    
                    # Replace placeholder in HTML
                    asset_path = f'"assets/img/temp/{selected_image}"'
                    result = result.replace(key, asset_path, 1)
                    logger.info("Replaced placeholder %s with image %s", key, selected_image)
            
            return result
        except Exception as e:
            logger.exception("Error processing image placeholders.")
            raise