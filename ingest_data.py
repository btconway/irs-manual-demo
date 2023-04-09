import sys
import os
import pinecone
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import DirectoryLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
import json


PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
PINECONE_API_ENV = os.environ.get('PINECONE_API_ENV')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
PINECONE_INDEX_NAME = os.environ.get('PINECONE_INDEX_NAME')


def load_documents(path_to_files):
    loader = DirectoryLoader(path=path_to_files, glob="*.json")
    raw_documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter()
    documents = text_splitter.split_documents(raw_documents)
    return documents


def send_docs_to_pinecone(documents):
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_API_ENV)
    index_name = "irs"

    for doc in documents:
        Pinecone.from_texts(json.loads(doc.page_content), embeddings, index_name=index_name)


if __name__ == "__main__":
    path_to_files = sys.argv[1]
    print(f"Grabbing json files from {path_to_files}")
    docs = load_documents(path_to_files)
    print(f"Found {len(docs)}, sending to pinecone")
    send_docs_to_pinecone(docs)








