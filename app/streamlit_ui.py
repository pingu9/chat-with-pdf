import streamlit as st
import requests
import os

from langchain_core.messages.chat import ChatMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory


from models import ModelManager

model_manager = ModelManager()

def print_messages():
    for chat_message in st.session_state.messages:
        st.chat_message(chat_message.role).write(chat_message.content)

def add_message(role, message):
    st.session_state.messages.append(ChatMessage(role=role, content=message))

def clear():
    st.session_state.clear()

# 세션 ID를 기반으로 세션 기록을 가져오는 함수
def get_session_history(session_ids):
    if session_ids not in st.session_state["store"]:  # 세션 ID가 store에 없는 경우
        # 새로운 ChatMessageHistory 객체를 생성하여 store에 저장
        st.session_state["store"][session_ids] = ChatMessageHistory()
    return st.session_state["store"][session_ids]  # 해당 세션 ID에 대한 세션 기록 반환


st.title("금융 마이데이터 Q&A 에이전트")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "store" not in st.session_state:
    st.session_state.store = {}

if "chain" not in st.session_state:
    st.session_state.chain = model_manager.get_chain()


print_messages()

question = st.chat_input("질문을 입력하세요:")

if question:
    st.chat_message("user").write(question)
#     chain = model_manager.get_chain()
    chain = st.session_state.chain

    chain_with_history = RunnableWithMessageHistory(
        chain,
        get_session_history,  # 세션 기록을 가져오는 함수
        input_messages_key="question",  # 사용자의 질문이 템플릿 변수에 들어갈 key
        history_messages_key="chat_history",  # 기록 메시지의 키
    )


    answer_stream = chain_with_history.stream(
        {"question": question},
        config={"configurable": {"session_id": "abc123"}},
    )


    with st.chat_message("assistant"):
        container = st.empty()
        answer = ""
        for token in answer_stream:
            answer += str(token)
            container.markdown(answer)
        add_message("user", question)
        add_message("assistant", answer)


if st.button("대화 기록 초기화"):
    clear()