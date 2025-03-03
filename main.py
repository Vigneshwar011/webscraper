
import streamlit as st
from scrape import (
    scrape_website, 
    split_dom_content, 
    clean_body_content, 
    extract_body_content
)
from parse import parse_with_ollama

st.title("AI Web Scraper")
url = st.text_input("Enter a Website URL: ")

if st.button("Scrape Site"):
    st.write("Scraping the website...")  # Text for status message
    result = scrape_website(url)
    body_content = extract_body_content(result)
    cleaned_content = clean_body_content(body_content)

    # Save cleaned content in session state
    st.session_state.dom_content = cleaned_content

    # Display the DOM content in an expandable section
    with st.expander("View DOM Content"):
        st.text_area("DOM Content", cleaned_content, height=300)

# Check if dom_content exists in session state
if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe what you want to parse?")

    if st.button("Parse Content"):
        if parse_description:
            st.write("Parsing the content...")
            dom_chunks = split_dom_content(st.session_state.dom_content)
            result = parse_with_ollama(dom_chunks, parse_description)
            st.write(result)
            
            # Assuming `split_dom_content` returns a list of chunks
            if dom_chunks:
                st.write(f"Parsed {len(dom_chunks)} chunks from the DOM content.")
                # Show the parsed content chunks (if needed)
                for idx, chunk in enumerate(dom_chunks):
                    st.write(f"Chunk {idx + 1}: {chunk[:500]}...")  # Display the first 500 chars of each chunk
            else:
                st.write("No chunks found to parse.")
        else:
            st.write("Please describe what you want to parse.")
