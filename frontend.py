# app.py

import streamlit as st
from backend import build_chatbot

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="YouTube ChatBot",
    page_icon="🎥",
    layout="centered"
)

# ---------------- TITLE ----------------

st.title("🎥 YouTube Video ChatBot")

st.write("Chat with any YouTube video using AI")

# ---------------- SESSION STATE ----------------

if "chain" not in st.session_state:
    st.session_state.chain = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.header("🔗 YouTube Video")

    youtube_url = st.text_input(
        "Paste YouTube URL"
    )

    process_btn = st.button(
        "Process Video"
    )

# ---------------- PROCESS VIDEO ----------------

if process_btn:

    if youtube_url == "":

        st.warning("Please enter YouTube URL")

    else:

        with st.spinner("Processing Video..."):

            try:

                chain = build_chatbot(youtube_url)

                st.session_state.chain = chain

                st.success("Video Ready For Chat ✅")

            except Exception as e:

                st.error(f"Error: {e}")

# ---------------- CHAT HISTORY ----------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# ---------------- USER INPUT ----------------

user_question = st.chat_input(
    "Ask question from video..."
)

# ---------------- CHAT ----------------

if user_question:

    if st.session_state.chain is None:

        st.warning("Please process a YouTube video first")

    else:

        # USER MESSAGE

        st.session_state.messages.append({
            "role": "user",
            "content": user_question
        })

        with st.chat_message("user"):

            st.markdown(user_question)

        # AI RESPONSE

        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                try:

                    response = st.session_state.chain.invoke(
                        user_question
                    )

                    st.markdown(response)

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response
                    })

                except Exception as e:

                    st.error(f"Error: {e}")