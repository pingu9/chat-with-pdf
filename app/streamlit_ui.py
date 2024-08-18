import streamlit as st
import requests

st.title("금융 마이데이터 Q&A")

question = st.text_input("질문을 입력하세요:")

if st.button("질문하기"):
    if question:
        response = requests.post("http://fastapi:8000/ask", json={"question": question})
        if response.status_code == 200:
            st.write("답변:", response.json()["answer"])
        else:
            st.write("에러:", response.status_code)

