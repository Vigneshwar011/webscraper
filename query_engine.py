from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains.question_answering import load_qa_chain
from langchain_openai import OpenAI  # Optional: Only needed if you're using OpenAI
from langchain.docstore.document import Document
from langchain.llms import HuggingFaceHub
import os

# Load the FAISS vector DB from disk
def load_vectorstore():
    embeddings = HuggingFaceEmbeddings()
    vectorstore = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    return vectorstore

# Ask question to LLM using retrieved context
def answer_question(query):
    vectorstore = load_vectorstore()

    # Get relevant documents for the question
    docs = vectorstore.similarity_search(query)

    # Load a QA chain with your LLM
    llm = HuggingFaceHub(
        repo_id="google/flan-t5-base",
        huggingfacehub_api_token="",  # 🔑 Add your token here
        model_kwargs={"temperature": 0.5}
    )

    chain = load_qa_chain(llm, chain_type="stuff")

    # Ask the LLM the question
    result = chain.run(input_documents=docs, question=query)
    return result


