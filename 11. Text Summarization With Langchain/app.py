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
    
url = st.text_input("URL", label_visibility="collapsed")


if st.button("Summarizee the Content from YT or Website"):
    ## Validate all the inputs
    if not groq_api_key.strip() or not url.strip():
        st.error("Please provide the information to get started")
    elif not validators.url(url):
        st.error("Please enter a valid URL. it can may be YT video url or website url")
        
    else:
        try:
            with st.spinner("Waiting..."):
                ## loading the website or YT video data
                if "youtube.com" in url:
                    loader = YoutubeLoader.from_youtube_url(url, add_video_info=True)
                else:
                    loader = UnstructuredURLLoader(urls=[url], ssl_verify=False,
                                                   header = {})