import streamlit as st
from src.providers.google_provider import GoogleLLMProvider
from src.parsers.comma_parser import CommaSeparatedParser
from src.parsers.json_parser import JsonParser
from src.templates.html_analysis import HtmlAnalysisTemplateBuilder
from src.templates.html_customization import HtmlCustomizationTemplateBuilder
from src.models.html_template import HtmlTemplate
from src.processor import LangChainProcessor
from src.html_processing.html_processing import HtmlProcessing

# Initialize the LLM provider
llm_provider = GoogleLLMProvider()

# Initialize html processor
html_processor = HtmlProcessing(r'data\test_html.html')

# remove css from the html content
html_content_without_css = html_processor.remove_html_styles()

# Create the processor
processor = LangChainProcessor(llm_provider, html_content_without_css)

# Generate questions
template_builder = HtmlAnalysisTemplateBuilder()
parser = CommaSeparatedParser()

list_of_questions = processor.generate_questions(template_builder, parser)

st.set_page_config(page_title='Web Editor', page_icon='💻', layout='centered')


if 'new_html' not in st.session_state:
    st.session_state.new_html = None

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

with open('templates/index.html', 'r', encoding='utf-8') as file:
    file = file.read()



def process_query(user_input):
    pass





chat_area, editor_area = st.tabs(['Code', 'Preview'])

with chat_area:
    chat_placeholder = st.empty()
    
    with chat_placeholder.container(height=500, border=True):
        # Display the chat history
        for author, message in st.session_state.chat_history:
            with st.chat_message(author):
                st.markdown(message)
        
        # Display the first question if just starting the questioning process
        if st.session_state.asking and len(st.session_state.chat_history) == 0:
            with st.chat_message("assistant"):
                st.markdown(list_of_questions[st.session_state.question_index])
            st.session_state.chat_history.append(("assistant", list_of_questions[st.session_state.question_index]))
    
    user_input = st.chat_input('Type a message...', key='ChatInput')
    
    if user_input:
        # Handle starting the questioning process
            st.session_state.chat_history.append(("user", user_input))
            text_to_the_user, updated_html = process_query(user_input)
            st.session_state.chat_history.append(("assistant", text_to_the_user))
            # Process the user's response to a question

with editor_area:
    if st.session_state.new_html:
        st.code(st.session_state.new_html, language='html')
        

# {'text_to_the_user' : , "updated_html"  :}