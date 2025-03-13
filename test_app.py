import streamlit as st

prompt = st.chat_input(
    "Say something and/or attach an image",
    accept_file=True,
    file_type=["html"],
)
if prompt and prompt.text:
    st.markdown(prompt.text)
if prompt and prompt["files"]:
    print(prompt["files"])
    st.markdown(prompt["files"][0])