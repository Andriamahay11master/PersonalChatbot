# api/qa_pipeline.py

from typing import List, Tuple
from .embeddings import embed_texts
from .vector_store import SimpleVectorStore


class QAPipeline:
    """
    Core Question-Answering pipeline using embeddings + vector search.
    Designed to be extended with an LLM and conversational memory.
    """

    def __init__(self, embedding_dim: int = 384):
        """
        Initialize the QA pipeline.

        Parameters
        ----------
        embedding_dim : int
            Dimension of the embedding vectors.
            Must match the embedding model output.
        """
        self.store = SimpleVectorStore(dim=embedding_dim)

    # ---------------------------------------------------------
    # Document ingestion
    # ---------------------------------------------------------
    def ingest_documents(self, texts: List[str]) -> None:
        """
        Ingest documents into the vector store.

        Parameters
        ----------
        texts : List[str]
            List of document texts.
        """
        if not texts:
            raise ValueError("No documents provided for ingestion.")

        embeddings = embed_texts(texts)
        self.store.add_embeddings(embeddings, texts)

    # ---------------------------------------------------------
    # Question answering
    # ---------------------------------------------------------
    def answer(self, query: str, session_id: str | None = None) -> Tuple[str, List[str]]:
        """
        Answer a user query using retrieved context.

        Parameters
        ----------
        query : str
            User query.
        session_id : str | None
            Optional session identifier for future memory support.

        Returns
        -------
        Tuple[str, List[str]]
            Generated answer and list of source documents.
        """
        if not query.strip():
            raise ValueError("Query must not be empty.")

        # Embed query
        query_embedding = embed_texts([query])[0]

        # Retrieve top-k relevant documents
        sources = self.store.search(query_embedding, k=3)

        # Build context
        context = "\n".join(sources) if sources else "No relevant documents found."

        # Prompt template (LLM-ready)
        prompt = (
            "You are a helpful assistant.\n"
            "Use the following context to answer the question.\n\n"
            f"Context:\n{context}\n\n"
            f"Question: {query}\n"
            "Answer:"
        )

        # -----------------------------------------------------
        # LLM CALL (stub for now)
        # -----------------------------------------------------
        # TODO:
        # Replace this with a real LLM call (OpenAI, Ollama, etc.)
        #
        # answer = llm.generate(prompt)
        # -----------------------------------------------------

        answer = (
            "This is a placeholder answer generated using retrieved context. "
            + (sources[0] if sources else "")
        )

        return answer, sources
