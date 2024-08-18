from langchain_openai import ChatOpenAI
from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import (
    ChatPromptTemplate, 
    HumanMessagePromptTemplate, 
    PromptTemplate
)
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_community.vectorstores import Chroma

from app.document_processor import load_documents
from langchain.text_splitter import CharacterTextSplitter
from langchain_core.output_parsers import StrOutputParser

documents = load_documents()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=50)

chroma_db_host = "http://chromadb"

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

prompt_template = PromptTemplate(
    input_variables=['question', 'context'],
    template=(
        "You are an assistant for question-answering tasks. "
        "Use the following pieces of retrieved context to answer the question. "
        "If you don't know the answer, just say that you don't know. "
        "Use three sentences maximum and keep the answer concise.\n"
    ),
    template_format='f-string',
    validate_template=True
)

prompt_template2 = PromptTemplate(
    input_variables=['question', 'context'],
    template=(
        "You are an assistant for question-answering tasks. "
        "Use the following pieces of retrieved context to answer the question. "
        "If you don't know the answer, just say that you don't know. "
        # "Use three sentences maximum and keep the answer concise.\n"
        "Please write your answer in a markdown format with the main points"
        "Be sure to include your source and page numbers in your answer."
        "Question: {question} \nContext: {context} \nAnswer:"

        """
        Example format:
        (table, if only needed)
        (answer to the question)

        **출처**
        - page source and page number

        """
    ),
    template_format='f-string',
    validate_template=True
)

# Define the HumanMessagePromptTemplate
human_message_prompt = HumanMessagePromptTemplate(prompt=prompt_template2)

# Define the ChatPromptTemplate using the HumanMessagePromptTemplate
rag_prompt = ChatPromptTemplate(
    input_variables=['question', 'context'],
    messages=[human_message_prompt]
)

# ChatGPT 모델 지정
llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

output_parser = StrOutputParser()

# pipe operator를 활용한 체인 생성
rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()} 
    | rag_prompt 
    | llm 
    | StrOutputParser()
)

class ModelManager:
    def __init__(self):
        self.model = rag_chain

    def generate_answer(self, prompt: str) -> str:
        return self.model.invoke(prompt)

model_manager = ModelManager()

