import streamlit as st
from src.llm_blocks.customize_json_data import customize_json_data
from src.html_process_manager import HtmlProcessManager
from src.utils.move_random_images import move_random_images

# # Save to specific path
save_path = r'technology-software_template\new_html.html'

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
            html_manager = HtmlProcessManager()
            json_placeholder = html_manager.get_json_placeholder(r'Placeholder_template\software_placeholders\placeholder.json')
            html_placeholder = html_manager.get_html_placeholder(r'Placeholder_template\software_placeholders\placeholder.html')
            
            updated_json = customize_json_data(business_name, business_description, json_placeholder)
            new_html = html_manager.geneate_new_html(updated_json, html_placeholder)
            # Generate new HTML using the updated JSON object
            new_html = html_manager.save_new_html(new_html , save_path)
            
            src_root_folder = r"Placeholder_template\software_images"
            dest_folder = r"technology-software_template\assets\img"
            move_random_images(src_root_folder, dest_folder)


        st.success("✅ HTML generated successfully!")
        
        with open(save_path, 'r', encoding='utf-8') as file:
            new_html = file.read()
        
        preview_url = f"http://localhost:5500/{save_path}"
            
        # Provide a link to open in a new tab
        st.markdown(f"### Preview Your Generated HTML")
        st.markdown(f'<a href="{preview_url}" target="_blank">Click here to open your HTML in a new tab</a>', unsafe_allow_html=True)

        # Display the HTML in an iframe
        st.markdown("### 🔍 Live Preview")
        print(new_html)
        st.components.v1.html(new_html, height=800, scrolling=True)
