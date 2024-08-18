import streamlit as st
import requests
import os

from langchain_core.messages.chat import ChatMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory



from models import ModelManager

model_manager = ModelManager()

session_id = "abc123" # 현재는 여러 개의 세션을 운영하지 않고 있기 때문에 임의의 값 지정

def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "store" not in st.session_state:
        st.session_state.store = {}

    if "chain" not in st.session_state:
        st.session_state.chain = model_manager.get_default_chain()

def print_messages():
    for chat_message in st.session_state.messages:
        st.chat_message(chat_message.role).write(chat_message.content)

def add_message(role, message):
    st.session_state.messages.append(ChatMessage(role=role, content=message))

def clear():
    st.session_state.clear()

# 세션 ID가 store에 없는 경우 새로운 ChatMessageHistory 객체를 생성하여 store에 저장
def get_session_history(session_ids):
    if session_ids not in st.session_state["store"]:
        st.session_state["store"][session_ids] = ChatMessageHistory()
    return st.session_state["store"][session_ids]  # 해당 세션 ID에 대한 세션 기록 반환


init_session_state()

st.title("금융 마이데이터 Q&A 에이전트")

print_messages()

question = st.chat_input("질문을 입력하세요:")

if question:
    st.chat_message("user").write(question)
    chain = st.session_state.chain

    chain_with_history = model_manager.get_chain_with_history(
        chain, get_session_history
    )

    answer_stream = chain_with_history.stream(
        {"question": question},
        config={"configurable": {"session_id": session_id}},
    )

    with st.chat_message("assistant"):
        container = st.empty()
        answer = ""
        for token in answer_stream:
            answer += token
            container.markdown(answer)
        add_message("user", question)
        add_message("assistant", answer)


if st.button("대화 기록 초기화"):
    clear()