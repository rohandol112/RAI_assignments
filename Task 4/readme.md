# Internship Assignment – Task 4: RAG Streamlit Application

## Problem Statement
Build a Streamlit-based Retrieval-Augmented Generation (RAG) application where users can upload multiple document types (PDF, DOCX, TXT) and interact with them using natural language questions. The application should parse, embed, and retrieve contextually relevant passages to generate accurate responses using a large language model.

## Objective
Design an AI-powered assistant that allows document comprehension through conversation. The key goal is to integrate a retrieval mechanism with a generative model to answer user queries using the uploaded documents.

## Solution Approach

### Step 1: Streamlit UI & File Upload
- Used `streamlit.file_uploader` with support for `.pdf`, `.docx`, and `.txt` formats.
- Enabled multiple file uploads simultaneously.
- A sidebar was created for file upload and processing controls.

### Step 2: Document Parsing
- PDF: Parsed using `PyPDF2`, reading all pages.
- DOCX: Parsed using `python-docx`, extracting all paragraphs.
- TXT: Read and decoded using standard UTF-8 encoding.
- Combined all extracted text into one large document string.

### Step 3: Text Chunking
- Implemented `RecursiveCharacterTextSplitter` from LangChain to break long text into overlapping chunks (chunk size: 1000, overlap: 300).
- This ensures better semantic embedding and retrieval performance.

### Step 4: Embedding and Vector Store
- Used Google Generative AI Embeddings via `langchain_google_genai.embeddings`.
- Stored all text embeddings using FAISS, a fast vector similarity library.
- Saved FAISS index locally for retrieval.

### Step 5: Retrieval-Augmented Generation (RAG)
- When a user enters a question, relevant document chunks are retrieved using semantic similarity from FAISS.
- Constructed a prompt that combines:
  - User’s current question
  - Chat history
  - Retrieved document chunks
- Passed this prompt to Gemini (gemini-1.5-flash) using `langchain_google_genai.ChatGoogleGenerativeAI`.
- Returned the model’s response to the user.

### Step 6: Chat Interface
- Used `st.chat_input` and `st.chat_message` to render a conversational interface.
- Maintained chat history using `streamlit.session_state` to provide continuity.
- Displayed both user and AI messages cleanly.

## Testing & Results
- Tested using combinations of PDF, DOCX, and TXT files.
- Questions were successfully answered based on the uploaded documents.
- Handled both single and multiple document scenarios.
- Verified proper error handling for no file upload or invalid input.

## Files

```
├── app.py                 # Main Streamlit application
├── utils.py               # Helper functions for parsing, chunking, embeddings, retrieval
├── config.py              # Loads Google API key
├── .env                   # Stores GOOGLE_API_KEY securely
├── requirements.txt       # All required Python libraries
├── faiss_index/           # Local FAISS index storage
└── README.md              # Assignment documentation
```

## Libraries Used
- streamlit
- langchain
- google-generativeai
- langchain-google-genai
- faiss-cpu
- PyPDF2, python-docx, dotenv


