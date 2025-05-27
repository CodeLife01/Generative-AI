import streamlit as st
import openai
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


import os
from dotenv import load_dotenv

load_dotenv()


## Langsmith tracking
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"]="Simple Q&A Chatbot With OpenAI V2"


## Prompt Template
prompt=ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistance. Please response to the user queries"),
        ("user","Question:{question}")
    ]
)

def generate_response(question,api_key,llm,temperature,max_token):
    openai.api_key=api_key
    llm=ChatOpenAI(model=llm)
    output_parser = StrOutputParser()
    chain=prompt | llm | output_parser
    answer = chain.invoke({"question":question})
    return answer

# --- App Title ---
st.title("🔍 Enhanced Q&A Chat with OpenAI")

# --- Sidebar Configuration ---
with st.sidebar:
    st.header("⚙️ Settings")
    
    api_key = st.text_input("🔑 OpenAI API Key", type="password")
    
    llm = st.selectbox("🤖 Choose a Model", ["gpt-4o", "gpt-4-turbo", "gpt-4"])
    
    temperature = st.slider("🎯 Temperature", 0.0, 1.0, 0.7)
    max_tokens = st.slider("📏 Max Tokens", 50, 300, 150)

# --- Main Interface ---
st.subheader("💬 Ask Your Question")

user_input = st.text_input("🧠 Your Question:")

# --- Handle User Input ---
if user_input:
    if api_key:
        response = generate_response(user_input, api_key, llm, temperature, max_tokens)
        st.success("✅ Response:")
        st.write(response)
    else:
        st.warning("⚠️ Please enter your OpenAI API key in the sidebar.")
else:
    st.info("💡 Enter a question above to get started.")
