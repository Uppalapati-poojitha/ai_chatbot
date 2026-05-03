import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.title("AI Chatbot")

# Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# System Prompt
role = st.selectbox(
    "Choose Assistant",
    ["Tutor", "Friend", "Coding Assistant"]
)

system_prompt = {
    "Tutor": "You are a helpful teacher.",
    "Friend": "You are a friendly companion.",
    "Coding Assistant": "You are an expert programmer."
}

# Display Chat
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# User Input
prompt = st.chat_input("Ask something...")

if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": system_prompt[role]
            }
        ] + st.session_state.messages
    )

    reply = response.choices[0].message.content

    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )

    st.rerun()

# Reset Button
if st.button("Reset Chat"):
    st.session_state.messages = []