import streamlit as st

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


# Streamlit app
st.set_page_config(page_title="Dynamic HTML Generator", layout="wide")

st.title("🧠 AI-Powered Business HTML Generator")

# Inputs
business_name = st.text_input("Enter your Business Name")
business_description = st.text_area("Enter your Business Description")

if st.button("🚀 Generate HTML"):
    if not business_name or not business_description:
        st.warning("Please fill in both fields before proceeding.")
    else:
        with st.spinner("Generating content with AI..."):
            api_key_loader = APIKeyLoader()
            model_loader = ModelLoader()
            prompt_loader = PromptLoader()
            chain_builder = ChainBuilder()
            
            json_placeholder_path = r'Placeholder_template\software_placeholders\placeholder.json'
            html_placeholder_path = r'Placeholder_template\software_placeholders\placeholder.html'
            # Save to specific path
            output_path = r'technology-software_template\new_html.html'
            
            json_placeholder = JsonFileReader().read(json_placeholder_path)
            
            customize_json_placeholder_llm =  CustomizeJsonPlaceholder(
                                    api_key_loader=api_key_loader,
                                    model_loader=model_loader,
                                    prompt_loader=prompt_loader,
                                    chain_builder=chain_builder
                                )
            
            updated_json = customize_json_placeholder_llm.run(business_name, business_description, json_placeholder)
            
            # Create an instance of HtmlProcessManager
            processor = HtmlProcessor(
                JsonFileReader(),
                TextFileReader(),
                TextFileWriter(),
                HtmlTemplate(),
                image_processor
            )
            
            new_html = processor.process(updated_json, html_placeholder_path, output_path)

        st.success("✅ HTML generated successfully!")
        
        with open(output_path, 'r', encoding='utf-8') as file:
            new_html = file.read()
        
        preview_url = f"http://localhost:5500/{output_path}"
            
        # Provide a link to open in a new tab
        st.markdown(f"### Preview Your Generated HTML")
        st.markdown(f'<a href="{preview_url}" target="_blank">Click here to open your HTML in a new tab</a>', unsafe_allow_html=True)

        # Display the HTML in an iframe
        st.markdown("### 🔍 Live Preview")
        print(new_html)
        st.components.v1.html(new_html, height=800, scrolling=True)
