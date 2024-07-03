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

def split_documents(documents: List[Document]) -> List[Document]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=310,
        chunk_overlap=100,
        length_function=len,
        is_separator_regex=False,
        add_start_index=True,
    )
    return text_splitter.split_documents(documents)

if __name__ == "__main__":
    documents = load_documents(directory_path)
    chunks = split_documents(documents)
    print(f"Total chunks: {len(chunks)}")
    print("First chunk:")
    print(chunks[0])