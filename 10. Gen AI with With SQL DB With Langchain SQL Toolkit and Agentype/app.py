import streamlit as st
from pathlib import Path
from langchain.agents import create_sql_agent
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_types import AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from sqlalchemy import create_engine
import sqlite3
from langchain_groq import ChatGroq

st.set_page_config(page_title="LangChain: Chat with SQL DB", page_icon="🐦")
st.title("🐦 LangChain: Chat with SQL DB")


INJECTION_WARNING = """
                    SQL agent can be vulberable to prompt injection. Use a DB role with limit
"""

LOCALDB = "USE_LOCALDB"
MYSQL = "USE_MYSQL"

radio_opt = ["Use SQlite3 Database.db", "Connect to your SQL Database"]

selected_opt = st.sidebar.radio(label="Choose the DB which you want to chat", options=radio_opt)

if radio_opt.index(selected_opt)==1:
    db_url = MYSQL
    mysql_host = st.sidebar.text_input("Provide My SQL Host")
    mysql_user = st.sidebar.text_input("MYSQL User")
    mysql_password = st.sidebar.text_input("MYSQL password", type="password")
    mysql_db = st.sidebar.text_input("MYSQL database")

else:
    db_url = LOCALDB
    
api_key = st.sidebar.text_input(label="Groq AI key",type="password")

if not db_url:
    st.info("Please enter the database information and url")
    
if not api_key:
    st.info("Please add the GROQ API key")
    
## LLM Model
llm = ChatGroq(groq_api_key = api_key, model_name = "Llama3-8b-8192", streaming=True)


@st.cache_resource(ttl="2h")
def configure_db(db_url,mysql_host=None,mysql_user=None,mysql_password=None,mysql_db=None):
    if db_url == LOCALDB:
        dbfilepath = (Path(__file__).parent/"student.db").absolute()
        print(dbfilepath)
        creator = lambda: sqlite3.connect(f"file:{dbfilepath}?mode=ro", uri=True)
        return SQLDatabase(create_engine("sqlite:///", creator=creator))
    elif db_url == MYSQL:
        if not(mysql_host or mysql_user or mysql_password or mysql_db):
            st.error("Please provide all MySQL connection details.")
            st.stop()  
        return SQLDatabase(create_engine(f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"))
    
if db_url == MYSQL:
    db = configure_db(db_url,mysql_host,mysql_user,mysql_password,mysql_db)
else:
    db=configure_db(db_url)
    
## Toolkit
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

agent = create_sql_agent(
    llm = llm,
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)

if "messages" not in st.session_state or st.sidebar.button("Clear message history"):
    st.session_state["messages"] = [{"role":"assistant", "content": "How can I help you?"}]
    
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

user_query = st.chat_input(placeholder="Ask anything from the database")

if user_query:
    st.session_state.messages.append({"role":"user", "content":user_query})
    st.chat_message("user").write(user_query)
    
    with st.chat_message("assistant"):
        Streamlit_Callback = StreamlitCallbackHandler(st.container())
        response = agent.run(user_query,callbacks=[Streamlit_Callback])
        st.session_state.messages.append({"role":"assistant", "content":response})
        st.write(response)