# api/embeddings.py
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List

# Load the embedding model once at startup
_model = None

def get_embedding_model():
    """Get or initialize the embedding model."""
    global _model
    if _model is None:
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model

def embed_texts(texts: List[str]) -> np.ndarray:
    """Embed texts using SentenceTransformer."""
    model = get_embedding_model()
    embeddings = model.encode(texts, convert_to_numpy=True)
    return embeddings.astype("float32")
