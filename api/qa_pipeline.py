# api/qa_pipeline.py
from .embeddings import embed_texts
from .vector_store import SimpleVectorStore

class QAPipeline:
    def __init__(self):
        self.store = SimpleVectorStore(dim=768)

    def ingest_documents(self, texts: List[str]):
        embs = embed_texts(texts)
        self.store.add_embeddings(embs, texts)

    def answer(self, query: str) -> tuple[str, List[str]]:
        q_emb = embed_texts([query])[0]
        sources = self.store.search(q_emb, k=3)
        # Build a simple prompt with sources
        context = "\n".join(sources)
        prompt = f"Use the following context to answer:\n{context}\nQuestion: {query}\nAnswer:"
        # Call LM here (stub)
        answer = "This is a placeholder answer using context: " + (sources[0] if sources else "no sources")
        return answer, sources
