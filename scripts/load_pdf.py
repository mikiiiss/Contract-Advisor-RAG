# from langchain_community.document_loaders import PyPDFLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter

# # Directory path
# directory_path = "data"  # Replace with the correct directory path if needed
# print("Directory path:", directory_path)

# # Load individual PDF files
# pdf_files = ["Raptor_Contract.pdf"]  # Replace with your PDF file names
# documents = []
# for file in pdf_files:
#     loader = PyPDFLoader(f"{directory_path}/{file}")
#     documents.extend(loader.load())

# def split_documents(documents: list):
#     text_splitter = RecursiveCharacterTextSplitter(
#         chunk_size=800,
#         chunk_overlap=80,
#         length_function=len,
#         is_separator_regex=False,
#     )
#     return text_splitter.split_documents(documents)

# if __name__ == "__main__":
#     chunks = split_documents(documents)
#     print(f"Total chunks: {len(chunks)}")
#     print("First chunk:")
#     print(chunks[0])

from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
from langchain.schema import Document
from langchain.docstore.document import Document
from langchain.text_splitter import NLTKTextSplitter, CharacterTextSplitter
import nltk
nltk.download('punkt')

# Directory path
directory_path = "data"  # Replace with the correct directory path if needed
print("Directory path:", directory_path)

# PDF files to load (if any)
pdf_files = ["Raptor_Contract.pdf"]  # Replace with your PDF file names

def load_documents(directory_path: str) -> List[Document]:
    documents = []
    
    # Load Markdown files
    loader = DirectoryLoader(directory_path, glob="*.md")
    documents.extend(loader.load())

    # Load PDF files
    for file in pdf_files:
        pdf_loader = PyPDFLoader(f"{directory_path}/{file}")
        documents.extend(pdf_loader.load())

    return documents

# def split_documents(documents: List[Document]) -> List[Document]:
#     text_splitter = RecursiveCharacterTextSplitter(
#         chunk_size=1000,
#         chunk_overlap=200,
#         length_function=len,
#         is_separator_regex=False,
#         add_start_index=True,
#     )
#     return text_splitter.split_documents(documents)
def split_documents(documents: List[Document]) -> List[Document]:
    # First, split the document into semantically coherent segments
    semantic_splitter = NLTKTextSplitter(
        length_function=len,
        add_start_index=True,
    )
    semantic_chunks = semantic_splitter.split_documents(documents)

    # Then, split the semantic chunks into smaller character-based chunks
    character_splitter = CharacterTextSplitter(
        chunk_size=230,  # Adjust this value based on your needs
        chunk_overlap=17,
        length_function=len,
        add_start_index=True,
    )

    final_chunks = []
    for chunk in semantic_chunks:
        final_chunks.extend(character_splitter.split_text(chunk.page_content))

    return final_chunks

if __name__ == "__main__":
    documents = load_documents(directory_path)
    chunks = split_documents(documents)
    print(f"Total chunks: {len(chunks)}")
    print("First chunk:")
    print(chunks[0])