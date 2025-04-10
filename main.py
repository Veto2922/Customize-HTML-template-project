from src.llm_blocks.custmize_json_placeholder import CustomizeJsonPlaceholder
from src.llm_blocks_helper.api_key_loader import APIKeyLoader
from src.llm_blocks_helper.model_loader import ModelLoader
from src.llm_blocks_helper.prompt_loader import PromptLoader
from src.llm_blocks_helper.chain_builder import ChainBuilder

from src.files_manager.html_processor import HtmlProcessor
from src.files_manager.helper import image_processor
from src.files_manager.helper.file_readers import JsonFileReader, TextFileReader
from src.files_manager.helper.file_writers import TextFileWriter
from src.files_manager.helper.html_template import HtmlTemplate

from traceback import format_exc
import os


class App:
    def __init__(self, business_name, business_description, json_placeholder_path, josn_image_description_path ,html_placeholder_path, output_path):
        """
        Initialize the App with necessary parameters.
        """
        self.business_name = business_name
        self.business_description = business_description
        self.json_placeholder_path = json_placeholder_path
        self.josn_image_description_path = josn_image_description_path
        self.html_placeholder_path = html_placeholder_path
        self.output_path = output_path

        # Initialize dependencies
        self.api_key_loader = APIKeyLoader()
        self.model_loader = ModelLoader()
        self.prompt_loader = PromptLoader()
        self.chain_builder = ChainBuilder()

    def run(self):
        """
        Execute the main logic of the application.
        """
        try:
            # Step 1: Read the JSON placeholder file
            json_placeholder = JsonFileReader().read(self.json_placeholder_path)
            json_image_description = JsonFileReader().read(self.josn_image_description_path)
            

            # Step 2: Customize the JSON placeholder using LLM
            customize_json_placeholder_llm = CustomizeJsonPlaceholder(
                                    api_key_loader=self.api_key_loader,
                                    model_loader=self.model_loader,
                                    prompt_loader=self.prompt_loader,
                                    chain_builder=self.chain_builder
                                )
            
            updated_json = customize_json_placeholder_llm.run(
                self.business_name, self.business_description, json_image_description  ,json_placeholder
            )

            # Step 3: Process HTML template with updated JSON data
            read_replace_and_write = HtmlProcessor(
                JsonFileReader(),
                TextFileReader(),
                TextFileWriter(),
                HtmlTemplate(),
                image_processor
            )
            new_html = read_replace_and_write.process(
                updated_json, self.html_placeholder_path, self.output_path
            )

            print(f"HTML file successfully generated at: {self.output_path}")

        except Exception as e:
            print(f"An error occurred: " , format_exc)


if __name__ == "__main__":
    # Example usage
    business_name = "Electro Pi"
    business_description = (
        "development of cutting-edge technology and AI solution and software. "
        "If you put any person images please put persons wearing glasses only."
    )

    json_placeholder_path = os.path.join( "Placeholder_template" ,"software_placeholders" , "placeholder.json" )
    html_placeholder_path = os.path.join('Placeholder_template' , 'software_placeholders' , 'placeholder.html')
    josn_image_description_path = os.path.join('Placeholder_template' , 'software_placeholders' , 'images_description.json')
    output_path = os.path.join('technology-software_template' , 'new_html.html')


    # Create an instance of the App class and run it
    app = App(business_name, business_description, json_placeholder_path,josn_image_description_path ,html_placeholder_path, output_path)
    app.run()