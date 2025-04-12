from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import OllamaLLM
import streamlit as st
import os


from dotenv import load_dotenv
load_dotenv()


## Langsmith tracking
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"]="Simple Q&A Chatbot With Ollama"


## Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistance. Please response to the user queries, answer only the question"),
        ("user","Question:{question}")
    ]
)

def generate_response(question,engine,temperature,max_token):
    llm=OllamaLLM(model=engine)
    output_parser = StrOutputParser()
    chain=prompt | llm | output_parser
    answer = chain.invoke({"question":question})
    return answer


## Title of the app
st.title("Enchanced Q&A Chat with Ollama")


## Sidebar fro setting
st.sidebar.title("settings")

## Drop download to select various Open AI models
engine = st.sidebar.selectbox("Select an Ollama Model",["gemma3:1b","gemma3"])

## Adjust response parameter
temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0,value=0.7)
max_tokens = st.sidebar.slider("Max Token", min_value=50, max_value=300, value=150)

## Main Interface fro User input
st.write("Ask Any Question")
user_input = st.text_input("You: ")


if user_input:
    response=generate_response(user_input,engine,temperature,max_tokens)
    st.write(response)
else:
    st.write("Please provide the query")