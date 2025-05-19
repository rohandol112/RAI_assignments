from PyPDF2 import PdfReader
from docx import Document
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter


def get_documents_text(files):
    text = ""
    for file in files:
        if file.type == "application/pdf":
            reader = PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() or ""
        elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = Document(file)
            for para in doc.paragraphs:
                text += para.text + "\n"
        elif file.type == "text/plain":
            text += file.read().decode("utf-8")
    return text


def get_text_chunks(text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=300)
    return splitter.split_text(text)


def get_vector_store(chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    store = FAISS.from_texts(chunks, embeddings)
    store.save_local("../faiss_index")


def get_conversational_chain():
    template = """
    Be accurate and detailed. If unsure, reply: 'answer is not available in the context'.
    Chat history:
    {chat_history}

    Context:
    {context}

    Question:
    {question}

    Answer:
    """
    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.5)
    prompt = PromptTemplate(template=template, input_variables=["context", "question", "chat_history"])
    return prompt | model | StrOutputParser()


def user_input(question, history):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    store = FAISS.load_local("../faiss_index", embeddings, allow_dangerous_deserialization=True)
    if not store:
        return "No documents found. Please upload and process files."
    docs = store.similarity_search(question)
    chain = get_conversational_chain()
    return chain.invoke({"chat_history": history, "context": docs, "question": question})
