# api/embeddings.py
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Optional
import torch

_model: Optional[SentenceTransformer] = None

def get_embedding_model(device: Optional[str] = None) -> SentenceTransformer:
    """
    Get or initialize the embedding model.
    """
    global _model

    if _model is None:
        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"

        _model = SentenceTransformer(
            "all-MiniLM-L6-v2",
            device=device
        )

    return _model

def embed_texts(
    texts: List[str],
    batch_size: int = 32,
    normalize: bool = True
) -> np.ndarray:
    """
    Embed a list of texts into float32 vectors.
    """
    if not texts:
        raise ValueError("`texts` must be a non-empty list of strings.")

    model = get_embedding_model()

    embeddings = model.encode(
        texts,
        batch_size=batch_size,
        convert_to_numpy=True,
        normalize_embeddings=normalize
    )

    return embeddings.astype("float32")
