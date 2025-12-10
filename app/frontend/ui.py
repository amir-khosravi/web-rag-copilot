import streamlit as st
import requests
import os
from app.config.settings import settings
from app.common.logger import get_logger

logger = get_logger(__name__)

# Reads from env var if available, defaults to localhost for local testing
BACKEND_HOST = os.getenv("BACKEND_HOST", "http://127.0.0.1:8000")
API_URL = f"{BACKEND_HOST}{settings.API_V1_STR}/chat"

st.set_page_config(page_title="Enterprise RAG Copilot", layout="centered")
st.title("Enterprise RAG Copilot Interface")

with st.sidebar:
    st.header("Model Configuration")
    selected_model = st.selectbox("Select Model:", settings.ALLOWED_MODEL_NAMES)
    system_prompt = st.text_area("System Prompt:", value="You are a helpful Enterprise AI assistant.", height=150)
    allow_web_search = st.toggle("Enable Web Search Tools")

user_query = st.chat_input("Enter your query here...")

if user_query:
    with st.chat_message("user"):
        st.markdown(user_query)

    payload = {
        "model_name": selected_model,
        "system_prompt": system_prompt,
        "messages": [user_query],
        "allow_search": allow_web_search
    }

    try:
        with st.spinner("Copilot is thinking..."):
            response = requests.post(API_URL, json=payload)
            if response.status_code == 200:
                agent_response = response.json().get("response", "No response")
                with st.chat_message("assistant"):
                    st.markdown(agent_response)
            else:
                st.error(f"Backend Service Error: {response.status_code}")

    except Exception as e:
        st.error("Failed to connect to Copilot Backend.")