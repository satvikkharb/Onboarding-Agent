import chromadb
from vectorstore.embedder import get_embedding

client = chromadb.PersistentClient(path="backend/vector_store/db")
collection = client.get_or_create_collection(name="faq")

def get_top_k_chunks(query: str, k=3) -> list:
    query_embedding = get_embedding(query)
    results = collection.query(query_embeddings=[query_embedding], n_results=k)
    return results['documents'][0] if results['documents'] else []
