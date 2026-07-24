import os
import tempfile

import streamlit as st

from llm.llm import generate_response
from rag.loader import load_document
from rag.splitter import split_documents
from rag.embeddings import get_embedding_model
from rag.vector_store import create_vector_store
from rag.retriever import get_retriever

# ---------------- Page Config ----------------

st.set_page_config(page_title="AI Research Assistant", page_icon="🤖")

st.title("🤖 AI Research Assistant")
st.write("Upload a PDF, DOCX, or TXT file and ask questions about its content.")

# ---------------- Session State ----------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "processed_file" not in st.session_state:
    st.session_state.processed_file = None

# ---------------- File Upload ----------------

uploaded_file = st.file_uploader(
    "Upload a document",
    type=["pdf", "docx", "txt"]
)

retriever = None

if uploaded_file is not None:

    file_type = uploaded_file.name.split(".")[-1].lower()

    # Only rebuild the vector store if this is a new file
    if st.session_state.processed_file != uploaded_file.name:

        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_type}") as temp_file:
            temp_file.write(uploaded_file.read())
            temp_path = temp_file.name

        with st.spinner("Processing document..."):

            documents = load_document(temp_path, file_type)
            chunks = split_documents(documents)
            embeddings = get_embedding_model()

            full_text = "\n\n".join(doc.page_content for doc in documents)

            # Short documents (resumes, short notes) fit entirely in the LLM's
            # context window, so skip similarity-based retrieval for them —
            # retrieval can miss sections a keyword-light question like
            # "how many projects" needs to see in full.
            st.session_state.full_text = full_text
            st.session_state.use_full_document = len(full_text) < 6000

            st.session_state.vector_store = create_vector_store(chunks, embeddings)
            st.session_state.retriever = get_retriever(st.session_state.vector_store)
            st.session_state.processed_file = uploaded_file.name
            st.session_state.doc_info = {
                "pages": len(documents),
                "chunks": len(chunks),
            }
            st.session_state.messages = []  # fresh chat for a new document

        os.unlink(temp_path)

    retriever = st.session_state.retriever

    st.success(f"'{uploaded_file.name}' loaded successfully!")
    st.caption(
        f"{st.session_state.doc_info['pages']} page(s) · "
        f"{st.session_state.doc_info['chunks']} chunk(s)"
    )

st.divider()

# ---------------- Chat History ----------------

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if message["role"] == "assistant" and message.get("sources"):
            with st.expander("Sources"):
                for src in message["sources"]:
                    st.markdown(f"**{src['label']}**")
                    st.write(src["text"])
                    st.divider()

# ---------------- Chat Input ----------------

user_query = st.chat_input("Ask a question about your document...")

if user_query:

    if uploaded_file is None or retriever is None:
        st.warning("Please upload a document first.")
    else:
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.write(user_query)

        with st.chat_message("assistant"):
            with st.spinner("Searching document..."):

                if st.session_state.get("use_full_document"):
                    # Small document: give the model everything, no retrieval gaps
                    context = st.session_state.full_text
                    sources = [{"label": "Full document", "text": context}]
                else:
                    results = retriever.invoke(user_query)
                    context = "\n\n".join(doc.page_content for doc in results)

                    sources = []
                    for i, doc in enumerate(results, start=1):
                        page = doc.metadata.get("page")
                        label = f"Source {i}" + (f" (page {page + 1})" if page is not None else "")
                        sources.append({"label": label, "text": doc.page_content})

                answer = generate_response(user_query, context)

            st.write(answer)
            with st.expander("Sources"):
                for src in sources:
                    st.markdown(f"**{src['label']}**")
                    st.write(src["text"])
                    st.divider()

        st.session_state.messages.append(
            {"role": "assistant", "content": answer, "sources": sources}
        )