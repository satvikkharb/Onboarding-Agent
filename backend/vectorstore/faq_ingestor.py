import os
import chromadb
from PyPDF2 import PdfReader
from embedder import get_embedding

CHROMA_PATH = "backend/vector_store/db"

client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_or_create_collection(name="faq")

def ingest_pdf_to_chroma(file_path: str):
    reader = PdfReader(file_path)
    pages = [page.extract_text() for page in reader.pages if page.extract_text()]
    
    for i, chunk in enumerate(pages):
        embedding = get_embedding(chunk)
        collection.add(
            documents=[chunk],
            embeddings=[embedding],
            ids=[f"faq_chunk_{i}"]
        )

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python3 faq_ingestor.py <path_to_pdf>")
    else:
        ingest_pdf_to_chroma(sys.argv[1])
        print("FAQ Ingestion Complete.")