import streamlit as st
import os
from src.files_manager.folder_archiver import ZipFolderArchiver

from main import App

# Streamlit app
st.set_page_config(page_title="Dynamic HTML Generator", layout="centered")

st.title("🧠 AI-Powered Business HTML Generator")

# Inputs
business_name = st.text_input("Enter your Business Name")
business_description = st.text_area("Enter your Business Description")

if st.button("🚀 Generate HTML"):
    if not business_name or not business_description:
        st.warning("Please fill in both fields before proceeding.")
    else:
        with st.spinner("Generating content with AI..."):
            
            json_placeholder_path = os.path.join( "Placeholder_template" ,"software_placeholders" , "placeholder.json" )
            html_placeholder_path = os.path.join('Placeholder_template' , 'software_placeholders' , 'placeholder.html')
            josn_image_description_path = os.path.join('Placeholder_template' , 'software_placeholders' , 'images_description.json')
            output_path = os.path.join('technology-software_template' , 'new_html.html')
            
            # Create an instance of the App class and run it
            app = App(business_name, business_description, json_placeholder_path,josn_image_description_path ,html_placeholder_path, output_path)
            app.run()

        st.success("✅ HTML generated successfully!")
        
        with open(output_path, 'r', encoding='utf-8') as file:
            new_html = file.read()
        
        
        # Provide a link to open in a new tab
        st.markdown(f"### Download Your Generated HTML")
        
        download_col1, download_col2 = st.columns(2)
        with download_col1:
            st.download_button(label="Download Only HTML",
                            data=new_html,
                            on_click='ignore',
                            file_name='index.html',
                            key="download-html",
                            use_container_width=True)
        
        with download_col2:
            # Create an archiver
            archiver = ZipFolderArchiver()
            
            # Archive the folder
            zip_data = archiver.archive('technology-software_template')
            
            # Provide a download button for the zip file
            zip_name = f'{business_name} Landing Page.zip'
            st.download_button(
                        label="Download All The Project",
                        data=zip_data,
                        file_name=zip_name,
                        mime="application/zip",
                        key="download-zip",
                        on_click="ignore",
                        use_container_width=True
                    )