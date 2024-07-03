# from embedding_function import get_embedding_function
# from langchain.vectorstores.chroma import Chroma
# import os
# import openai
# from langchain_openai import OpenAIEmbeddings
# CHROMA_PATH = "chroma"
# DATA_PATH = "data"
# openai_api_key = os.getenv('OPENAI_API_KEY')

# def save_to_chroma(chunks: list[Document]):
#     # Clear out the database first.
#     if os.path.exists(CHROMA_PATH):
#         shutil.rmtree(CHROMA_PATH)

#     # Create a new DB from the documents.
#     db = Chroma.from_documents(
#         chunks, OpenAIEmbeddings(), persist_directory=CHROMA_PATH
#     )
#     db.persist()
#     print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")

# from langchain.document_loaders import DirectoryLoader
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
import openai
from dotenv import load_dotenv
import os
import shutil
from typing import List
from load_pdf import load_documents,split_documents  # Import necessary functions
import pysqlite3
import sys
sys.modules['sqlite3'] = pysqlite3

# Load environment variables. Assumes that project contains .env file with API keys
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')


CHROMA_PATH = "chroma"
DATA_PATH = "data"

def main():
    generate_data_store()

def generate_data_store():
    documents = load_documents(DATA_PATH)
    chunks = split_documents(documents)
    save_to_chroma(chunks)

def save_to_chroma(chunks: List[Document]):
    # Clear out the database first.
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    # Create a new DB from the documents.
    db = Chroma.from_documents(
        chunks, OpenAIEmbeddings(), persist_directory=CHROMA_PATH
    )
    db.persist()
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")

if __name__ == "__main__":
    main()