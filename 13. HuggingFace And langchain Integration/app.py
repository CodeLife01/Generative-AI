import validators, streamlit as st
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader, UnstructuredURLLoader

from langchain_huggingface import HuggingFaceEndpoint

## Streamlit APP
st.set_page_config(page_title="LangChain: Summarize Text From YT or website", page_icon="🐦")
st.title("🐦 LangChain: Summarize Text From YT or Website")
st.subheader("Summarize URL")


## Get the Groq API Key asn URL (YT or website) to be Summarized
with st.sidebar:
    hf_api_key = st.text_input("HuggingFace API Token", value="", type="password")

url = st.text_input("URL", label_visibility="collapsed")

## Gemma Model Using Groq API
#llm = ChatGroq(model="llama-3.3-70b-versatile", groq_api_key=groq_api_key)

repo_id = "Qwen/Qwen3-32B"
llm = HuggingFaceEndpoint(
    repo_id=repo_id, 
    max_length=150, 
    temperature=0.7, 
    token=hf_api_key,
    task="text-generation",
    )

prompt_template = """
Provide summarize of the following content in 300 words:
Content:{text}

"""

prompt = PromptTemplate(template=prompt_template, input_variables=["text"])

if st.button("Summarizee the Content from YT or Website"):
    ## Validate all the inputs
    if not hf_api_key.strip() or not url.strip():
        st.error("Please provide the information to get started")
    elif not validators.url(url):
        st.error("Please enter a valid URL. It can may be YT video url or website url")
        
    else:
        try:
            with st.spinner("Waiting..."):
                ## loading the website or YT video data
                if "youtube.com" in url:
                    loader = YoutubeLoader.from_youtube_url(url, add_video_info=True)
                else:
                    loader = UnstructuredURLLoader(urls=[url], ssl_verify=False,
                                                   header = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"})
                docs = loader.load()
                
                ## Chain for summarization
                chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt)
                output_summary = chain.run(docs)
                
                st.success(output_summary)
                
        except Exception as e:
            st.exception(f"Exception:{e}")