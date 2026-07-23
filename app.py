import streamlit as st
import tempfile

from llm.llm import generate_response
from rag.loader import load_pdf

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

    st.success("PDF Loaded Successfully!")

    st.subheader("Document Information")

    st.write(f"Total Pages: {len(documents)}")

    st.success("Document loaded successfully and is ready for processing.")

st.divider()

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