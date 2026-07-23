import streamlit as st
import tempfile

from llm.llm import generate_response
from rag.loader import load_pdf
from rag.splitter import split_documents
from rag.embeddings import get_embedding_model
from rag.vector_store import create_vector_store

# Page title
st.set_page_config(page_title="AI Research Assistant")

# Heading
st.title("🤖 AI Research Assistant")

st.write("Ask any question to the AI.")

# ---------------- PDF Upload ----------------

uploaded_file = st.file_uploader(
    "Upload a PDF",
    type=["pdf"]
)

if uploaded_file is not None:

    # Save uploaded PDF temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(uploaded_file.read())
        temp_path = temp_file.name

    # Load PDF
    documents = load_pdf(temp_path)
    chunks = split_documents(documents) 
    
    embeddings = get_embedding_model()
    vector_store = create_vector_store(
    chunks,
    embeddings
)

    st.success("PDF Loaded Successfully!")

    st.subheader("Document Information")

    st.write(f"Total Pages: {len(documents)}")
    st.write(f"Total Chunks: {len(chunks)}")
    st.success("Vector store created successfully!")

    
st.divider()
embeddings = get_embedding_model()

# ---------------- Chatbot ----------------

user_query = st.text_input("Enter your question:")

if st.button("Ask"):

    if user_query.strip():

        with st.spinner("Generating response..."):
            answer = generate_response(user_query)

        st.success("Response Generated!")
        st.write(answer)

    else:
        st.warning("Please enter a question.")