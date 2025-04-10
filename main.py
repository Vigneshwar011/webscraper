import streamlit as st
from scrape import (
    scrape_website,
    split_dom_content,
    clean_body_content,
    extract_body_content
)
from parse import parse_with_ollama
from database import create_table, insert_parsed_data
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document
import os


create_table()

st.title("AI Web Scraper & Database Storage")

url = st.text_input("Enter a Website URL:")

if st.button("Scrape Site"):
    st.write("🔍 Scraping the website...")
    result = scrape_website(url)
    body_content = extract_body_content(result)
    cleaned_content = clean_body_content(body_content)

    st.session_state.dom_content = cleaned_content

    with st.expander("🔹 View DOM Content"):
        st.text_area("DOM Content", cleaned_content, height=300)

if "dom_content" in st.session_state:
    parse_description = st.text_area(" Describe what you want to parse:")

    if st.button("Parse Content"):
        if parse_description:
            st.write(" Parsing the content...")
            dom_chunks = split_dom_content(st.session_state.dom_content)
            parsed_result = parse_with_ollama(dom_chunks, parse_description)

            # Save to DB
            insert_parsed_data(url, parsed_result)

            #  Create and Save FAISS index
            st.write(" Creating FAISS vector index...")
            embeddings = HuggingFaceEmbeddings()
            documents = [Document(page_content=chunk) for chunk in dom_chunks]
            vectorstore = FAISS.from_documents(documents, embeddings)
            vectorstore.save_local("faiss_index")

            st.write(" Parsing, Storage & Vector Index Creation Complete.")
        else:
            st.warning(" Please describe what you want to parse.")

# Q&A Section
if os.path.exists("faiss_index/index.faiss"):
    question = st.text_input("🤖 Ask a Question Based on Parsed Website")

    if question:
        from query_engine import answer_question
        answer = answer_question(question)
        st.success(answer)
else:
    st.info("ℹ️ Please parse content before asking questions.")

