from langchain_community.document_loaders import PyMuPDFLoader
import os

import requests
from tempfile import NamedTemporaryFile


# def load_documents():
#     documents = []
#     for file_name in os.listdir("data"):
#         if file_name.endswith(".pdf"):
#             file_path = os.path.join("data", file_name)
#             loader = PyMuPDFLoader(file_path)
#             pages = loader.load()
#             documents.append(pages)
#     return documents

pdf_urls = ['https://www.mydatacenter.or.kr:3441/cmmn/fileBrDownload?id=JHuKqjlWK0e%2FH9Yi7ed09GsZWL6TiRKp9yg4qGj%2FKFmV9RC6j8RJdh6I8JAqzoFv&type=2', 'https://www.mydatacenter.or.kr:3441/cmmn/fileBrDownload?id=dKi%2B7cAM4PO8JA4z7jwm4AoM07vmQIbSKQ9EvM0DPRYokFCd%2BhLigsDUZ0hQopjD&type=2']

# 주어진 pdf url을 통하여 document의 리스트 로드하여 반환한다.
def load_documents():
    documents = []

    for url in pdf_urls:
        # Download the PDF file
        response = requests.get(url)
        response.raise_for_status()  # Ensure the request was successful

        with NamedTemporaryFile(delete=True, suffix=".pdf") as temp_pdf:
            temp_pdf.write(response.content)
            temp_pdf.flush()  # Ensure all data is written

            loader = PyMuPDFLoader(temp_pdf.name)
            pages = loader.load()
            documents.append(pages)

    return documents