import streamlit as st
import tempfile

from llm.llm import generate_response
from rag.loader import load_pdf
from rag.splitter import split_documents
from rag.embeddings import get_embedding_model
from rag.vector_store import create_vector_store
from rag.retriever import get_retriever

# ---------------- Page Config ----------------

st.set_page_config(page_title="AI Research Assistant")

st.title("🤖 AI Research Assistant")
st.write("Upload a PDF and ask questions about its content.")

# ---------------- PDF Upload ----------------

uploaded_file = st.file_uploader(
    "Upload a PDF",
    type=["pdf"]
)

retriever = None

if uploaded_file is not None:

    # Save uploaded PDF temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(uploaded_file.read())
        temp_path = temp_file.name

    # Load PDF
    documents = load_pdf(temp_path)

    # Split into chunks
    chunks = split_documents(documents)

    # Load embedding model
    embeddings = get_embedding_model()

    # Create vector store
    vector_store = create_vector_store(
        chunks,
        embeddings
    )

    # Create retriever
    retriever = get_retriever(vector_store)

    st.success("PDF Loaded Successfully!")

    st.subheader("Document Information")

    st.write(f"Total Pages: {len(documents)}")
    st.write(f"Total Chunks: {len(chunks)}")

    st.success("Vector Store Created Successfully!")

st.divider()

# ---------------- Chatbot ----------------

user_query = st.text_input("Enter your question:")

if st.button("Ask"):

    if uploaded_file is None:
        st.warning("Please upload a PDF first.")

    elif not user_query.strip():
        st.warning("Please enter a question.")

    else:

        with st.spinner("Searching document..."):

            # Retrieve relevant chunks
            results = retriever.invoke(user_query)

            # Combine chunks into one context
            context = "\n\n".join(
                doc.page_content for doc in results
            )

            # Generate answer using RAG
            answer = generate_response(
                user_query,
                context
            )

        st.success("Response Generated!")

        st.write(answer)

        with st.expander("Retrieved Context"):

            for i, doc in enumerate(results, start=1):
                st.markdown(f"### Chunk {i}")
                st.write(doc.page_content)
                st.divider()