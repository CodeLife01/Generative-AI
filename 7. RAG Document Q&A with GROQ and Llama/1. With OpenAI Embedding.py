import streamlit as st
import os
import time
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFDirectoryLoader

# Load environment variables
load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

# --- LLM Setup ---
llm = ChatGroq(groq_api_key=groq_api_key, model_name="Llama3-8b-8192")

# --- Prompt Template ---
prompt = ChatPromptTemplate.from_template(
    """
    Answer the questions based only on the context provided.
    <context>
    {context}
    </context>
    Question: {input}
    """
)

# --- Embedding Creation Function ---
def create_vector_embedding():
    with st.spinner("🔄 Creating vector embeddings from PDFs..."):
        if "vectors" not in st.session_state:
            st.session_state.embeddings = OpenAIEmbeddings()
            st.session_state.loader = PyPDFDirectoryLoader("research_papers")
            st.session_state.docs = st.session_state.loader.load()
            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            final_docs = splitter.split_documents(st.session_state.docs[:50])
            st.session_state.vectors = FAISS.from_documents(final_docs, st.session_state.embeddings)
            st.success("✅ Vector database ready!")

# --- UI Layout ---
st.set_page_config(page_title="RAG Q&A with LLaMA3", layout="wide")
st.title("📚 RAG Document Q&A with Groq & LLaMA3")

tab1, tab2 = st.tabs(["🔧 Embed Documents", "❓ Ask Questions"])

with tab1:
    st.markdown("Upload and embed your PDF research papers into a vector database.")

    if st.button("📄 Create Document Embeddings"):
        create_vector_embedding()

    if "vectors" in st.session_state:
        st.success("Embeddings are ready! Switch to the next tab to ask questions.")

with tab2:
    if "vectors" not in st.session_state:
        st.warning("⚠️ Please embed documents first in the 'Embed Documents' tab.")
    else:
        user_prompt = st.text_input("🔍 Enter your query:")
        if user_prompt:
            with st.spinner("🧠 Thinking..."):
                document_chain = create_stuff_documents_chain(llm, prompt)
                retriever = st.session_state.vectors.as_retriever()
                retrieval_chain = create_retrieval_chain(retriever, document_chain)

                start = time.process_time()
                response = retrieval_chain.invoke({"input": user_prompt})
                elapsed = time.process_time() - start

                st.success(f"✅ Answer (in {elapsed:.2f}s):")
                st.write(response["answer"])

                with st.expander("📂 Document Similarity Context"):
                    for i, doc in enumerate(response["context"]):
                        st.markdown(f"**Snippet {i+1}:**")
                        st.write(doc.page_content)
                        st.markdown("---")
