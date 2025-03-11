import streamlit as st
import subprocess

st.set_page_config(page_title='Web Editor', page_icon='💻', layout='wide')

if 'ques_is_aval' not in st.session_state:
    st.session_state.ques_is_aval = False


with open('templates/index.html', 'r', encoding='utf-8') as file:
    file = file.read()

list_of_questions = ['What is the desired brand name- logo text for the website header and footer?',
                     'What wording should be used for the main heading (H1) on the hero section of the landing page?',
                     'What descriptive text should accompany the main heading in the hero section to explain the business offering?',
                     'What call-to-action text should be used on the primary button in the hero section?',
                     'What heading should be used for the "Features" section to best describe the benefits offered?',
                     'What wording should be used for each of the individual feature titles- for example- Smart Automation- Advanced Analytics- Enterprise Security?',
                     'What wording should be used for the "Testimonials" section heading to convey customer satisfaction?',
                     'What is the desired wording for the call-to-action heading and supporting text in the email collection section?',
                     'What placeholder text should be used in the email input field of the email collection form?',
                     'What wording should be used for the navigation links (e.g.- Features- Testimonials- Pricing- Contact)?']

def get_questions(list_of_questions):
    result = {}
    user_input = ChatInputPlaceholder.chat_input('Answer The Quesion...', key='QuestionAnswer')
    for question in list_of_questions:
        with st.chat_message('assistant'):
          st.markdown(question)
        if user_input:
          with st.chat_message('user'):
            st.markdown(user_input)
        result[question] = user_input
    return result


with st.container(border=True, height=550, key='MainContainer'):
  chat_area, editor_area = st.columns(2)

  with chat_area:
    with st.container(border=True, height=500, key='ChatContainer'):
      MessageContainerPlaceholder = st.empty()
      ChatInputPlaceholder = st.empty()
      user_input = ChatInputPlaceholder.chat_input('Type a message...', key='ChatInput')
      
      if user_input:
        with st.chat_message('user'):
          st.markdown(user_input)
        with MessageContainerPlaceholder.container(border=True, height=400, key='MessageContainer'):
          # if st.button('Preview', key='SaveButton'):
          #         subprocess.call(["python", "-m", "webbrowser", "index.html"])
          if 'hi' in user_input:
            ques_dict = get_questions(list_of_questions)
  
  with editor_area:
      with st.container(border=True, key='EditorContainer'):
          st.code(file, language='html')