import streamlit as st
from scrape import (
    scrape_website, 
    split_dom_content, 
    clean_body_content, 
    extract_body_content
)
from parse import parse_with_ollama
from database import create_table, insert_parsed_data  # Import database functions

#  Create the database table when the app starts
create_table()

st.title("AI Web Scraper & Database Storage")

url = st.text_input("Enter a Website URL: ")

if st.button("Scrape Site"):
    st.write("🔍 Scraping the website...")
    result = scrape_website(url)
    body_content = extract_body_content(result)
    cleaned_content = clean_body_content(body_content)

    st.session_state.dom_content = cleaned_content

    with st.expander("🔹 View DOM Content"):
        st.text_area("DOM Content", cleaned_content, height=300)

if "dom_content" in st.session_state:
    parse_description = st.text_area("✍️ Describe what you want to parse:")

    if st.button("Parse Content"):
        if parse_description:
            st.write("🔄 Parsing the content...")
            dom_chunks = split_dom_content(st.session_state.dom_content)
            result = parse_with_ollama(dom_chunks, parse_description)
            
            # ✅ Store parsed data in the database
            response = insert_parsed_data(url, result)
            st.write(response)

            st.write("✅ Parsing & Database Storage Complete.")
        else:
            st.write("⚠️ Please describe what you want to parse.")

