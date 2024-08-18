from langchain.prompts import ChatPromptTemplate

def load_prompt():
    return ChatPromptTemplate.from_template(
        "You are an assistant for question-answering tasks. "
        "Use the following pieces of retrieved context to answer the question. "
        "If you don't know the answer, just say that you don't know. "
        "Please write your answer in a markdown format with the main points. "
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