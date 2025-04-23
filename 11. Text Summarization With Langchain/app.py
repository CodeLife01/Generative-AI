import validators, streamlit as st
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader, UnstructuredURLLoader


## Streamlit APP
st.set_page_config(page_title="LangChain: Summarize Text From YT or website", page_icon="🐦")
st.title("🐦 LangChain: Summarize Text From YT or Website")
st.subheader("Summarize URL")


## Get the Groq API Key asn URL (YT or website) to be Summarized
with st.sidebar:
    groq_api_key = st.text_input("Groq API Key", value="", type="password")
    
url = st.text_input("")