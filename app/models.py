from langchain_openai import ChatOpenAI
from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import (
    ChatPromptTemplate, 
    HumanMessagePromptTemplate, 
    PromptTemplate,
    MessagesPlaceholder
)
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_community.vectorstores import Chroma

from document_processor import load_documents
from langchain.text_splitter import CharacterTextSplitter
from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter

documents = load_documents()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=50)

chroma_db_host = "http://chromadb:8001"

# 임베딩
embeddings = OpenAIEmbeddings()

# embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

for document in documents:
    texts = text_splitter.split_documents(document)
    # docsearch = Chroma.from_documents(
    #     documents = texts,
    #     embeddings = embeddings,
    #     client_settings = {"chroma_server" : chroma_db_host}
    # )
    docsearch = Chroma.from_documents(
        texts,
        embeddings
    )


# retriever 가져옴
retriever = docsearch.as_retriever()

def create_chain():
    prompt = ChatPromptTemplate.from_template(
        "You are an assistant for question-answering tasks. "
        "Use the following pieces of retrieved context to answer the question. "
        "If you don't know the answer, just say that you don't know. "
        "Please write your answer in a markdown format with the main points"
        "Be sure to include your source and page numbers in your answer."
        "Previous Chat History: {chat_history} Question: {question}\nContext: {context} \nAnswer:"

        """
        Example format:
        (table, if only needed)
        (answer to the question)

        **출처**
        - page source and page number

        """
    )

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

    def get_chain(self):
        return self.model

model_manager = ModelManager()

