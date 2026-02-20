import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv

# ===== LOAD ENV =====
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("API key missing")
    st.stop()

client = Groq(api_key=api_key)

# ===== PAGE =====
st.set_page_config(page_title="AI Security Assistant", layout="wide")

st.title("AI Cybersecurity Assistant")

# ===== CHAT HISTORY STORAGE =====
if "messages" not in st.session_state:
    st.session_state.messages = []

# ===== MODE SELECT =====
mode = st.radio("Select Mode", ["Chat Assistant", "Log Analyzer"])

# ================= CHAT MODE =================
if mode == "Chat Assistant":

    st.subheader("Cybersecurity Chat Assistant")

    # Show history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # User input
    user_input = st.chat_input("Ask security question...")

    if user_input:

        # Save user message
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

        with st.chat_message("user"):
            st.write(user_input)

        # AI Response
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=st.session_state.messages
        )

        ai_reply = response.choices[0].message.content

        st.session_state.messages.append({
            "role": "assistant",
            "content": ai_reply
        })

        with st.chat_message("assistant"):
            st.write(ai_reply)

# ================= LOG ANALYZER =================
else:

    st.subheader("Security Log Analyzer")

    uploaded_file = st.file_uploader("Upload Log File", type=["txt"])
    log_text = st.text_area("Or paste log here")

    log_data = ""

    if uploaded_file:
        log_data = uploaded_file.read().decode("utf-8")

    if log_text:
        log_data = log_text

    if st.button("Analyze Log"):

        if log_data:

            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "system",
                        "content": "You are cybersecurity SOC analyst. Analyze logs and give risk level, threat type and explanation."
                    },
                    {
                        "role": "user",
                        "content": log_data
                    }
                ]
            )

            result = response.choices[0].message.content

            st.success("Analysis Complete")
            st.write(result)

        else:
            st.warning("Provide log data")
