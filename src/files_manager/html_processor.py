from src.Log_Manager.log_manager import get_logger
from src.files_manager.helper.base import FileReader, FileWriter
from src.files_manager.helper.html_template import HtmlTemplate
from src.files_manager.helper.image_processor import ImagePlaceholderProcessor


logger = get_logger(__name__)

class HtmlProcessor:
    """Main class for HTML processing with dependencies injected"""
    def __init__(self, json_reader:FileReader, html_reader:FileReader, html_writer:FileWriter, template_engine:HtmlTemplate, image_processor:ImagePlaceholderProcessor = None):
        self.json_reader = json_reader
        self.html_reader = html_reader
        self.html_writer = html_writer
        self.template_engine = template_engine
        self.image_processor = image_processor
        logger.info("HtmlProcessor initialized.")

    def process(self, json_placeholder, template_path, output_path):
        """Process HTML template with JSON data and save result"""
        try:
            # Load data
            template = self.html_reader.read(template_path)
            
            # Process template
            processed_html = self.template_engine.replace_placeholders(template, json_placeholder)
            
            # Save result
            self.html_writer.write(processed_html, output_path)
            
            return processed_html
        except Exception as e:
            logger.exception("HTML processing failed.")
            raise
    
    def process_with_images(self, json_path, template_path, output_path, image_json_path, src_image_folder, dest_image_folder):
        """Process HTML template with JSON data and images, then save result"""
        try:
            if self.image_processor is None:
                logger.error("Image processor not provided for image processing task")
                raise ValueError("Image processor is required for process_with_images method")
            
            # Load data
            placeholders = self.json_reader.read(json_path)
            template = self.html_reader.read(template_path)
            image_placeholders = self.json_reader.read(image_json_path)
            
            # Process template with text placeholders
            processed_html = self.template_engine.replace_placeholders(template, placeholders)
            
            # Process image placeholders
            final_html = self.image_processor.process_image_placeholders(
                processed_html, 
                image_placeholders, 
                src_image_folder, 
                dest_image_folder
            )
            
            # Save result
            self.html_writer.write(final_html, output_path)
            
            return final_html
        except Exception as e:
            logger.exception("HTML processing with images failed.")
            raise