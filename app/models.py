from langchain_openai import ChatOpenAI

from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter

from retriever import get_retriever
from prompt import load_prompt

retriever = get_retriever()

def create_chain():
    prompt = load_prompt()

    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

    chain = (
        {
            "context": itemgetter("question") | retriever,
            "question": itemgetter("question"),
            "chat_history": itemgetter("chat_history"),
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain

class ModelManager:
    def __init__(self):
        self.model = create_chain()

    #
    def get_default_chain(self):
        return self.model

    def get_chain_with_history(self, chain, get_session_history):
        return RunnableWithMessageHistory(
            chain,
            get_session_history,
            input_messages_key="question",
            history_messages_key="chat_history",
        )

model_manager = ModelManager()

