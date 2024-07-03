import os
import openai
import numpy as np
from dotenv import load_dotenv

from langchain.embeddings import OpenAIEmbeddings

def get_embedding_function():
    load_dotenv()
    openai_api_key = os.getenv('OPENAI_API_KEY')
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    return embeddings
