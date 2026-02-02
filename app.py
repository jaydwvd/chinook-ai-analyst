import streamlit as st
import os
import requests
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI

# ==========================================
# 1. PAGE SETUP
# ==========================================
st.set_page_config(page_title="Chinook AI Analyst", page_icon="🕵️‍♂️")
st.title("🕵️‍♂️ Chinook AI Data Analyst")

# ==========================================
# 2. CONFIGURATION & DATABASE
# ==========================================
# Retrieve the API Key from environment or allow user to input it
api_key = os.environ.get("OPENAI_API_KEY")

if not api_key:
    api_key = st.sidebar.text_input("OpenAI API Key", type="password")
    if not api_key:
        st.info("Please add your OpenAI API Key to continue.")
        st.stop()
    os.environ["OPENAI_API_KEY"] = api_key


@st.cache_resource
def get_db_agent():
    """
    Initializes the Database and Agent.
    Cached so it doesn't reload on every message.
    """
    # 1. Ensure DB file exists
    if not os.path.exists("Chinook.db"):
        url = "https://storage.googleapis.com/benchmarks-artifacts/chinook/Chinook.db"
        response = requests.get(url)
        with open("Chinook.db", "wb") as f:
            f.write(response.content)

    # 2. Connect to DB
    db = SQLDatabase.from_uri("sqlite:///Chinook.db")

    # 3. Setup LLM and Toolkit
    # Using gpt-4o-mini as it's cheaper and fast
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)

    # 4. Create Agent
    agent_executor = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True,
        handle_parsing_errors=True
    )
    return agent_executor


# Load the agent
try:
    agent = get_db_agent()
except Exception as e:
    st.error(f"Error loading database: {e}")
    st.stop()

# ==========================================
# 3. CHAT INTERFACE
# ==========================================

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant",
                                     "content": "Hi! I'm connected to the Chinook database. Ask me anything about sales, customers, or tracks!"}]

# Display existing chat messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])

# Handle user input
user_query = st.chat_input("Ask your data question here...")

if user_query:
    # 1. Display user message
    st.session_state.messages.append({"role": "user", "content": user_query})
    st.chat_message("user").write(user_query)

    # 2. Generate and display response
    with st.chat_message("assistant"):
        st_callback = st.container()  # container for potential callbacks/loading
        with st.spinner("Analyzing database..."):
            try:
                response = agent.invoke(user_query)
                answer = response["output"]
                st.write(answer)

                # Save context
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"An error occurred: {e}")