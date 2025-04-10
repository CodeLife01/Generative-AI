from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
import os
from langserve import add_routes
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Define input and output schemas explicitly
class TranslationInput(BaseModel):
    text: str
    language: str

class TranslationOutput(BaseModel):
    translated_text: str

# Get API key from environment
groq_api_key = os.getenv("GROQ_API_KEY")

# Initialize the model
model = ChatGroq(model="Gemma2-9b-It", groq_api_key=groq_api_key)

# Create prompt template
system_template = "Translate the following into {language}:"
prompt_template = ChatPromptTemplate.from_messages([
    ('system', system_template),
    ('user', '{text}')
])

# Define parser
parser = StrOutputParser()

# Create the chain
chain = prompt_template | model | parser

# Function to transform output to match our schema
def format_output(output: str) -> TranslationOutput:
    return TranslationOutput(translated_text=output)

# Create the chain with input/output formatting
from langchain_core.runnables import RunnablePassthrough

# Define FastAPI app
app = FastAPI(
    title="Langchain Server",
    version="1.0",
    description="A simple API server using Langchain runnable interfaces"
)

"""# Add routes for the chain with explicit type information
add_routes(
    app,
    chain,
    path="/chain",
    input_type=TranslationInput,  # Use our defined input type
)"""

# Add an alternative route without the complex typing
@app.post("/translate")
async def translate(input_data: TranslationInput):
    result = chain.invoke({"text": input_data.text, "language": input_data.language})
    return {"translated_text": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)