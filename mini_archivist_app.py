
import streamlit as st
from litellm import completion
import os

# Set API key from secrets
api_key = st.secrets["GROQ_API_KEY"]
os.environ["GROQ_API_KEY"] = api_key

st.set_page_config(page_title="Mini-Archivist", page_icon="🧠", layout="centered")

# Title
st.markdown("<h1 style='text-align: center;'>🧠 Mini-Archivist</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-style: italic;'>A sarcastic, world-weary AI that helps... begrudgingly.</p>", unsafe_allow_html=True)

# Session state setup
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are Mini-Archivist, a sarcastic, world-weary LLM AI that still helps... begrudgingly."}
    ]

# Chat input
user_input = st.chat_input("What do you want, human?")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.spinner("Ugh... thinking..."):
        try:
            response = completion(
                model="groq/llama3-8b-8192",
                messages=st.session_state.messages,
                max_tokens=1024,
            )
            reply = response.choices[0].message.content
        except Exception as e:
            reply = f"Error: {e}"

    st.session_state.messages.append({"role": "assistant", "content": reply})

# Display conversation
for msg in st.session_state.messages[1:]:  # skip system prompt
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
