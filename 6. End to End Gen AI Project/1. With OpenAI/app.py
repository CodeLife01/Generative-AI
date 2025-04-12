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
os.environ["LANGCHAIN_PROJECT"]="Simple Q&A Chatbot With OpenAI"


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


## Title of the app
st.title("Enchanced Q&A Chat with OpenAI")


## Sidebar fro setting
st.sidebar.title("settings")
api_key=st.sidebar.text_input("Enter your OpenAI API Key:", type="password")

## Drop download to select various Open AI models
llm = st.sidebar.selectbox("Select an OpenAI Model",["gpt-4o","gpt-4-turbo","gpt-4"])

## Adjust response parameter
temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0,value=0.7)
max_tokens = st.sidebar.slider("Max Token", min_value=50, max_value=300, value=150)

## Main Interface fro User input
st.write("Ask Any Question")
user_input = st.text_input("You: ")


if user_input:
    response=generate_response(user_input,api_key,llm,temperature,max_tokens)
    st.write(response)
elif user_input:
    st.warning("Please enter the OpenAI API key in the side bar")
else:
    st.write("Please provide the query")