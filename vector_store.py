import chromadb
from sentence_transformers import SentenceTransformer
from typing import List, Dict
from urllib.parse import urlparse
import os

class VectorStore:
    def __init__(self, embedding_model_name="sentence-transformers/all-MiniLM-L6-v2"):
        # Optionally swap in a faster or quantized model here for CPU use.
        self.client = chromadb.Client()
        self.collection = self.client.create_collection(name="documents")
        self.embedding_model = SentenceTransformer(embedding_model_name)
        self.cache = {}  # Simple cache for repeated queries

    def add_documents(self, chunks: List[Dict], metadata_extra: List[Dict] = None):
        texts = [chunk['text'] for chunk in chunks]
        embeddings = self.embedding_model.encode(texts, batch_size=32, normalize_embeddings=True).tolist()
        metadatas = [{"chunk_id": chunk['chunk_id']} for chunk in chunks]
        if metadata_extra:
            # Merge extra metadata into per-chunk metadata if provided.
            for i, meta in enumerate(metadata_extra):
                metadatas[i].update(meta)
        ids = [str(i) for i in range(len(chunks))]
        self.collection.add(documents=texts, embeddings=embeddings, metadatas=metadatas, ids=ids)

    def similarity_search(self, query: str, k: int = 5, metadata_filter: dict = None) -> List[Dict]:
        # Optional: cache for hot queries
        cache_key = (query, k, frozenset(metadata_filter.items()) if metadata_filter else None)
        if cache_key in self.cache:
            return self.cache[cache_key]

        # Embedding (normalize for cosine search speed)
        query_embedding = self.embedding_model.encode([query], normalize_embeddings=True).tolist()
        # Dynamic metadata filtering, if needed
        if metadata_filter:
            results = self.collection.query(
                query_embeddings=query_embedding, n_results=k, where=metadata_filter
            )
        else:
            results = self.collection.query(query_embeddings=query_embedding, n_results=k)

        # Structured, explainable results
        contexts = []
        for i in range(len(results['documents'][0])):
            context = {
                "text": results['documents'][0][i],
                "relevance_score": 1 - results['distances'][0][i],
                "metadata": results['metadatas'][0][i],
                "id": results['ids'][0][i],  # Track ID for evidence trace
            }
            # Add more info if needed (e.g., page number, heading)
            contexts.append(context)
        # Fast cache for repeat queries
        self.cache[cache_key] = contexts
        return contexts
