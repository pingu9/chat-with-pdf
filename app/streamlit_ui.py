import streamlit as st
import requests

from langchain_core.messages.chat import ChatMessage

from models import ModelManager

model_manager = ModelManager()

st.title("금융 마이데이터 Q&A 에이전트")

if "messages" not in st.session_state:
    st.session_state.messages = []

def print_message(message):
    for chat_message in st.session_state.messages:
        st.chat_message(chat_message.role).write(chat_message.content)

def add_message(role, message):
    st.session_state.messages.append(ChatMessage(role=role, content=message))


question = st.chat_input("질문을 입력하세요:")

if question:
    answer_stream = model_manager.generate_answer_stream(question)
    with st.chat_message("assistant"):
        container = st.empty()
        answer = ""
        for token in answer_stream:
            answer += token
            container.markdown(answer)

    add_message("user", question)
