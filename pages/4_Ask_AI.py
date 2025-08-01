import streamlit as st
import requests
import os
from dotenv import find_dotenv, load_dotenv

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

st.set_page_config(page_title="Chat", layout="centered")

# Set Groq API key
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
MODEL = "llama3-8b-8192"

def chatbot_ui():
    # Session state to store messages
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Sidebar actions
    with st.sidebar:
        if st.button("🗑️ Clear chat"):
            st.session_state.chat_history = []

    # Chat container
    st.markdown("<h3 style='text-align:center;'>💬 Chat with a Bot</h3>", unsafe_allow_html=True)
    chat_container = st.container()

    # Display chat history
    for msg in st.session_state.chat_history:
        role, content = msg["role"], msg["content"]
        align = "flex-end" if role == "user" else "flex-start"
        bg = "#3B82F6" if role == "user" else "#374151"
        color = "white"
        chat_container.markdown(
            f"""
            <div style='display:flex; justify-content:{align};'>
                <div style='background:{bg}; color:{color}; padding:10px; border-radius:10px; max-width:80%; margin:5px;'>
                    {content}
                </div>
            </div>
            """, unsafe_allow_html=True
        )

    # User input
    user_input = st.chat_input("Type your message...")

    # Send message to Groq API
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        # Prepare messages
        messages = [{"role": msg["role"], "content": msg["content"]} for msg in st.session_state.chat_history]

        # Call Groq API
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": MODEL,
                "messages": messages,
                "temperature": 0.7
            }
        )

        assistant_reply = response.json()["choices"][0]["message"]["content"]
        st.session_state.chat_history.append({"role": "assistant", "content": assistant_reply})
        st.rerun()

chatbot_ui()
