# api/embeddings.py
import numpy as np

def embed_texts(texts: List[str]) -> np.ndarray:
    # Replace with real embedding call
    # Example: return np.array([model.encode(t) for t in texts])
    # Placeholder: random vectors
    dim = 768
    return np.random.randn(len(texts), dim).astype("float32")
