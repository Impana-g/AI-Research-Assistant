# 🤖 AI Research Assistant (RAG with LLMs)

A smart research assistant that answers questions about your own documents using
Retrieval-Augmented Generation (RAG). Upload a file, ask a question in plain
English, and get an answer grounded in the document — with the exact source
chunks shown alongside it.

## Description

Upload a PDF, DOCX, or TXT file and chat with it. The assistant retrieves the
most relevant passages from your document and uses an LLM to generate an
accurate, grounded answer — refusing to guess when the answer isn't in the
document.

## Tech Stack

- **Python**
- **LangChain** (`langchain-community`, `langchain-text-splitters`, `langchain-huggingface`)
- **FAISS** for vector storage and similarity search
- **HuggingFace Sentence Transformers** (`all-MiniLM-L6-v2`) for embeddings
- **OpenAI-compatible LLM API** via OpenRouter
- **Streamlit** for the chat UI

## Key Features

- 📄 Upload PDF, DOCX, or TXT files
- 💬 Ask questions in natural language, in a chat-style interface with full conversation history
- 🔍 Retrieves the most relevant chunks and generates accurate, context-grounded answers
- 📚 Displays the retrieved source chunks (with page numbers where available) behind every answer, so you can verify credibility
- 🧠 Automatically re-indexes when you upload a new document, and resets the conversation

## How It Works

1. **Load** — the uploaded file is parsed into text (`rag/loader.py`)
2. **Split** — text is chunked with overlap for better retrieval (`rag/splitter.py`)
3. **Embed** — chunks are embedded with a HuggingFace sentence-transformer model (`rag/embeddings.py`)
4. **Store & Retrieve** — chunks are indexed in FAISS and the top-k most relevant are retrieved per question (`rag/vector_store.py`, `rag/retriever.py`)
5. **Generate** — the retrieved context and question are passed to the LLM, which answers only from that context (`llm/llm.py`)

## Setup

1. Clone the repo and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file in the project root:
   ```
   OPENROUTER_API_KEY=your_api_key_here
   MODEL_NAME=your_model_name_here
   ```
   (Get an API key from [OpenRouter](https://openrouter.ai/); `MODEL_NAME` is
   any chat model available on OpenRouter, e.g. `openai/gpt-4o-mini`.)

3. Run the app:
   ```bash
   streamlit run app.py
   ```

4. Open the local URL Streamlit prints, upload a document, and start asking questions.

## Resume Impact

Demonstrates practical knowledge of RAG pipelines, vector databases (FAISS),
embedding models, and LLM API integration in a working end-to-end application.

## Roadmap / Not Yet Implemented

- Live web search / real-time source retrieval (currently document-only)
- Multi-document upload in a single session