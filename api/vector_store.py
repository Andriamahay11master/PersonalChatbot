# api/vector_store.py

import faiss
import numpy as np
from typing import List


class SimpleVectorStore:
    """
    Simple in-memory FAISS-based vector store.
    Stores embeddings and their corresponding documents.
    """

    def __init__(self, dim: int, index_path: str | None = None):
        """
        Initialize the vector store.

        Parameters
        ----------
        dim : int
            Dimension of embedding vectors.
        index_path : str | None
            Optional path for future persistence.
        """
        self.dim = dim

        # Use inner product for cosine similarity (with normalized vectors)
        self.index = faiss.IndexFlatIP(dim)

        self.documents: List[str] = []
        self.index_path = index_path

    # ---------------------------------------------------------
    # Add embeddings
    # ---------------------------------------------------------
    def add_embeddings(self, embeddings: np.ndarray, docs: List[str]) -> None:
        """
        Add embeddings and corresponding documents to the index.
        """
        if len(embeddings) != len(docs):
            raise ValueError("Number of embeddings must match number of documents.")

        if embeddings.ndim != 2 or embeddings.shape[1] != self.dim:
            raise ValueError(
                f"Embeddings must have shape (n, {self.dim}). "
                f"Got {embeddings.shape}."
            )

        # Ensure embeddings are float32
        embeddings = embeddings.astype("float32")

        # Normalize for cosine similarity
        faiss.normalize_L2(embeddings)

        self.index.add(embeddings)
        self.documents.extend(docs)

    # ---------------------------------------------------------
    # Search
    # ---------------------------------------------------------
    def search(self, query_embedding: np.ndarray, k: int = 5) -> List[str]:
        """
        Search for top-k most similar documents.
        """
        if self.index.ntotal == 0:
            return []

        if query_embedding.ndim == 1:
            query_embedding = query_embedding.reshape(1, -1)

        if query_embedding.shape[1] != self.dim:
            raise ValueError(
                f"Query embedding dimension mismatch. "
                f"Expected {self.dim}, got {query_embedding.shape[1]}."
            )

        query_embedding = query_embedding.astype("float32")
        faiss.normalize_L2(query_embedding)

        distances, indices = self.index.search(query_embedding, k)

        results: List[str] = []
        for idx in indices[0]:
            if 0 <= idx < len(self.documents):
                results.append(self.documents[idx])

        return results
