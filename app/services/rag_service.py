from rag.pdf_reader import extract_pdf_text
from rag.chunker import create_chunks
from rag.vector_store import (
    store_chunks,
    search_chunks,
    get_chunk_count
)


class RAGService:

    @staticmethod
    def upload_pdf(uploaded_file):

        pdf_text = extract_pdf_text(uploaded_file)

        chunks = create_chunks(pdf_text)

        store_chunks(chunks)

        return {
            "characters": len(pdf_text),
            "chunks": len(chunks),
            "stored": get_chunk_count()
        }

    @staticmethod
    def retrieve(query):

        return search_chunks(query)