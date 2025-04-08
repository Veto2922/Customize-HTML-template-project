from src.llm_blocks.custmize_json_placeholder import CustomizeJsonPlaceholder
from src.html_process_manager import HtmlProcessManager
from src.utils.move_random_images import move_random_images

if __name__ == "__main__":
    # Example usage
    business_name = "Electro Pi"
    business_description = "development of cutting-edge technology and AI solution and software."
    
    # Call the function with the example data
    
    # Create an instance of HtmlProcessManager
    html_manager = HtmlProcessManager()
    json_placeholder = html_manager.get_json_placeholder(r'Placeholder_template\software_placeholders\placeholder.json')
    html_placeholder = html_manager.get_html_placeholder(r'Placeholder_template\software_placeholders\placeholder.html')
    # print(json_placeholder)
    # print(html_placeholder)
    customize_json_placeholder_llm =  CustomizeJsonPlaceholder()
    updated_json = customize_json_placeholder_llm.run(business_name, business_description, json_placeholder)
    new_html = html_manager.geneate_new_html(updated_json, html_placeholder)
    print('this is json from model  ' , updated_json)
    # Example usage
    src_root_folder = r"Placeholder_template\software_images"
    dest_folder = r"technology-software_template\assets\img"
    move_random_images(src_root_folder, dest_folder)
    
    
    # Generate new HTML using the updated JSON object
    html_manager.save_new_html(new_html , r'technology-software_template\new_html.html')

    # Print the updated JSON object
    



