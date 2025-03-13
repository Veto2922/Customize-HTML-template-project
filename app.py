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

# list_of_questions = ['What is the desired brand name- logo text for the website header and footer?',
#                      'What wording should be used for the main heading (H1) on the hero section of the landing page?',
#                      'What descriptive text should accompany the main heading in the hero section to explain the business offering?',
#                      'What call-to-action text should be used on the primary button in the hero section?',
#                      'What heading should be used for the "Features" section to best describe the benefits offered?',
#                      'What wording should be used for each of the individual feature titles- for example- Smart Automation- Advanced Analytics- Enterprise Security?',
#                      'What wording should be used for the "Testimonials" section heading to convey customer satisfaction?',
#                      'What is the desired wording for the call-to-action heading and supporting text in the email collection section?',
#                      'What placeholder text should be used in the email input field of the email collection form?',
#                      'What wording should be used for the navigation links (e.g.- Features- Testimonials- Pricing- Contact)?']

st.set_page_config(page_title='Web Editor', page_icon='💻', layout='centered')

if 'ques_is_aval' not in st.session_state:
    st.session_state.ques_is_aval = False

if 'asking' not in st.session_state:
    st.session_state.asking = False

if 'question_answerd' not in st.session_state:
    st.session_state.question_answerd = False

if 'question_index' not in st.session_state:
    st.session_state.question_index = 0

if 'new_html' not in st.session_state:
    st.session_state.new_html = None

if 'ques_dict' not in st.session_state:
    st.session_state.ques_dict = None

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

with open('templates/index.html', 'r', encoding='utf-8') as file:
    file = file.read()


def get_questions(user_input):
    result = {}
    if st.session_state.asking and user_input:
        # Add the user's response to the chat history
        st.session_state.chat_history.append(("user", user_input))
        
        # Store the answer for the current question
        result[list_of_questions[st.session_state.question_index]] = user_input
        
        # Move to the next question
        st.session_state.question_index += 1
        
        # If we have more questions, add the next one to the chat history
        if st.session_state.question_index < len(list_of_questions):
            st.session_state.chat_history.append(("assistant", list_of_questions[st.session_state.question_index]))
        else:
            st.session_state.asking = False
            st.session_state.question_answerd = True
            st.session_state.chat_history.append(("assistant", "Thank you for answering all questions!"))
            
    return result

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
        if user_input and not st.session_state.asking:
            st.session_state.asking = True
            st.session_state.question_index = 0
            st.session_state.chat_history.append(("user", user_input))
            st.session_state.chat_history.append(("assistant", list_of_questions[0]))
            st.rerun()
        else:
            # Process the user's response to a question
            st.session_state.ques_dict = get_questions(user_input)
            st.rerun()
        
    if st.session_state.question_answerd:
      # Customize HTML with responses
      json_parser = JsonParser(HtmlTemplate)
      customization_builder = HtmlCustomizationTemplateBuilder(json_parser.get_format_instructions())
      
      customized_html = processor.customize_html(
          customization_builder,
          json_parser,
          st.session_state.ques_dict
      )
      
      st.session_state.new_html = html_processor.replace_html_body(customized_html['html_template'])
      print(st.session_state.new_html)

with editor_area:
    if st.session_state.new_html:
      st.code(st.session_state.new_html, language='html')