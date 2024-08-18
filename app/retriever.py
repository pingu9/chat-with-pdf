from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from document_processor import load_documents
from langchain.text_splitter import CharacterTextSplitter

def get_retriever():
    documents = load_documents()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=50)

    # 임베딩
    embeddings = OpenAIEmbeddings()
    # embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    texts = []
    for document in documents:
        texts.extend(text_splitter.split_documents(document))

    docsearch = Chroma.from_documents(
        texts,
        embeddings
    )

    return docsearch.as_retriever()