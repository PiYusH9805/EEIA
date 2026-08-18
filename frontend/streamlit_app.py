import os
import sys
import time

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from app.main import chat, upload_document

# ----------------------------------------------------
# Page Config
# ----------------------------------------------------

st.set_page_config(
    page_title="EEIA",
    page_icon="🤖",
    layout="wide"
)

# ----------------------------------------------------
# Stream Response Animation
# ----------------------------------------------------

def response_generator(text):

    for word in text.split():

        yield word + " "

        time.sleep(0.02)

# ----------------------------------------------------
# UI
# ----------------------------------------------------

st.title("🤖 Enterprise Engineering Intelligence Agent")

st.markdown(
    "AI-Powered Software Engineering Assistant"
)

# ----------------------------------------------------
# Clear Chat
# ----------------------------------------------------

if st.button("🗑 Clear Chat"):

    st.session_state.messages = []

    st.rerun()

# ----------------------------------------------------
# Memory
# ----------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pdf_uploaded" not in st.session_state:
    st.session_state.pdf_uploaded = False

if "uploaded_file_name" not in st.session_state:
    st.session_state.uploaded_file_name = None

# ----------------------------------------------------
# Show Previous Messages
# ----------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# ----------------------------------------------------
# Sidebar
# ----------------------------------------------------

st.sidebar.title("📄 Document Upload")

uploaded_file = st.sidebar.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

if uploaded_file:

    # Upload only once
    if (
        not st.session_state.pdf_uploaded
        or st.session_state.uploaded_file_name != uploaded_file.name
    ):

        with st.spinner("Uploading PDF..."):

            stats = upload_document(uploaded_file)

        st.session_state.pdf_uploaded = True
        st.session_state.uploaded_file_name = uploaded_file.name
        st.session_state.pdf_stats = stats

    stats = st.session_state.pdf_stats

    st.sidebar.success("✅ PDF Loaded Successfully")

    st.sidebar.write(f"Characters : {stats['characters']}")
    st.sidebar.write(f"Chunks : {stats['chunks']}")
    st.sidebar.write(f"Stored : {stats['stored']}")



# ----------------------------------------------------
# Chat Input
# ----------------------------------------------------

prompt = st.chat_input("Ask anything...")

if prompt:

    # -------------------------------
    # Show User Message
    # -------------------------------

    with st.chat_message("user"):

        st.markdown(prompt)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    try:

        # -------------------------------
        # PDF Query Detection
        # -------------------------------

        pdf_keywords = [

            "pdf",
            "document",
            "file",
            "question",
            "q1",
            "q2",
            "q3",
            "summary",
            "summarize"

        ]

        is_pdf_query = any(
            keyword in prompt.lower()
            for keyword in pdf_keywords
        )

        # -------------------------------
        # Build Final Prompt
        # -------------------------------

        if uploaded_file and is_pdf_query:

            final_prompt = prompt

        else:

            final_prompt = prompt

        # -------------------------------
        # Planner Agent
        # -------------------------------

        st.write("Calling Planner...")

        answer = chat(final_prompt)

        st.write("Answer:", answer)

    except Exception as e:

        answer = f"❌ {str(e)}"



# ----------------------------------------------------
# Assistant Response
# ----------------------------------------------------

        with st.chat_message("assistant"):

            st.write_stream(
                response_generator(answer)
            )

# ----------------------------------------------------
# Save Conversation
# ----------------------------------------------------

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )