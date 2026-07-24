from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader,
)


def load_document(file_path, file_type):
    """
    Load a document (PDF, DOCX, or TXT) and return its pages/content.
    """

    if file_type == "pdf":
        loader = PyPDFLoader(file_path)
    elif file_type == "docx":
        loader = Docx2txtLoader(file_path)
    elif file_type == "txt":
        loader = TextLoader(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")

    documents = loader.load()

    return documents