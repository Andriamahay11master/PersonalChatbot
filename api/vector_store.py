# api/vector_store.py
import faiss
import numpy as np
from typing import List

class SimpleVectorStore:
    def __init__(self, dim: int, index_path: str = "data/index.faiss"):
        self.index = faiss.IndexFlatL2(dim)
        self.documents = []  # parallel list of docs or metadata
        self.index_path = index_path

    def add_embeddings(self, embeddings: np.ndarray, docs: List[str]):
        self.index.add(embeddings)
        self.documents.extend(docs)

    def search(self, query_emb: np.ndarray, k: int = 5):
        D, I = self.index.search(query_emb, k)
        results = [self.documents[i] for i in I[0] if i < len(self.documents)]
        return results
