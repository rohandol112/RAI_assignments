import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from utils import user_input, get_documents_text, get_text_chunks, get_vector_store
from config import get_google_api_key, load_config
import google.generativeai as genai

load_config()
genai.configure(api_key=get_google_api_key())

st.set_page_config(page_title="Document Chat", page_icon="📄")
st.header("📄 Chat with Documents")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Hi there! Upload PDF, DOCX, or TXT files to start chatting.")
    ]

for msg in st.session_state.chat_history:
    with st.chat_message("AI" if isinstance(msg, AIMessage) else "Human"):
        st.write(msg.content)

user_question = st.chat_input("Ask something about your documents")
if user_question:
    st.session_state.chat_history.append(HumanMessage(content=user_question))
    with st.chat_message("Human"):
        st.write(user_question)

    response = user_input(user_question, st.session_state.chat_history)
    with st.chat_message("AI"):
        st.write(response)
    st.session_state.chat_history.append(AIMessage(content=response))

with st.sidebar:
    st.title("Upload Files")
    files = st.file_uploader("Upload PDF, DOCX, or TXT", type=["pdf", "docx", "txt"], accept_multiple_files=True)
    if st.button("Process"):
        if files:
            with st.spinner("Reading and indexing documents..."):
                text = get_documents_text(files)
                chunks = get_text_chunks(text)
                get_vector_store(chunks)
                st.success("Ready to chat!")
        else:
            st.warning("Please upload at least one file.")
