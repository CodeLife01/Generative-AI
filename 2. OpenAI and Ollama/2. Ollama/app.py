import os
from dotenv import load_dotenv
from langchain_community.llms import Ollama
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load environment variables
load_dotenv()

# Langsmith Tracking
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")

# Define prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Please respond to the question asked."),
        ("user", "Question: {question}")
    ]
)

# Streamlit app configuration
st.set_page_config(
    page_title="Langchain Demo with Gemma3",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling the interface
st.markdown("""
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f7f7f7;
        }
        .stButton button {
            background-color: #4CAF50;
            color: white;
            font-size: 18px;
            font-weight: bold;
            border-radius: 8px;
            padding: 12px 20px;
            transition: background-color 0.3s ease;
        }
        .stButton button:hover {
            background-color: #45a049;
        }
        .stTextInput input {
            background-color: #ffffff;
            border-radius: 6px;
            padding: 12px;
            border: 1px solid #ddd;
            width: 100%;
            font-size: 16px;
        }
        .stTextInput input:focus {
            border-color: #0078D4;
        }
        .stMarkdown {
            color: #333;
            font-size: 18px;
            line-height: 1.6;
        }
        .stTitle {
            color: #333;
            font-size: 28px;
            font-weight: 700;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# App title
st.title("🌟 Langchain Demo with Gemma3 🤖")

# Input section
input_text = st.text_input(
    "What question would you like to ask the model?",
    placeholder="Type your question here...",
    label_visibility="collapsed"
)

# Create a submit button for better interaction
submit_button = st.button("Get Answer")

# If button is pressed and input exists
if submit_button and input_text:
    # Instantiate the Ollama model
    llm = Ollama(model="gemma3")
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser
    
    # Show loading spinner while processing
    with st.spinner('Processing your question...'):
        response = chain.invoke({"question": input_text})
    
    # Display the model's response
    st.markdown(f"### Answer: \n{response}")
    
# Optional: Add a footer or extra section for guidance or credits
st.markdown("""
    ---
    **Powered by Langchain & Gemma3**  
    Try different questions to explore the capabilities of the model!
""", unsafe_allow_html=True)
