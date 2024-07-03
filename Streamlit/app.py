import streamlit as st
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
import pysqlite3
import sys
sys.modules['sqlite3'] = pysqlite3

# Load environment variables
load_dotenv()

CHROMA_PATH = "chroma"
PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

# Streamlit App
st.title("Question & Answer System")

question = st.text_input("Enter your question:")
if st.button("Get Answer"):
    if question:
        # Prepare the DB
        embedding_function = OpenAIEmbeddings()
        db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

        # Search the DB
        results = db.similarity_search_with_relevance_scores(question, k=3)
        if len(results) == 0 or results[0][1] < 0.7:
            st.write("Unable to find matching results.")
        else:
            context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
            prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
            prompt = prompt_template.format(context=context_text, question=question)
            
            model = ChatOpenAI()
            response_text = model.invoke(prompt)
            
            sources = [doc.metadata.get("source", None) for doc, _score in results]
            formatted_response = f"Response: {response_text}\nSources: {sources}"
            
            # Display context and answer
            st.subheader("Context")
            st.write(context_text)
            st.subheader("Answer")
            st.write(response_text)
            st.subheader("Sources")
            st.write(sources)
    else:
        st.write("Please enter a question.")