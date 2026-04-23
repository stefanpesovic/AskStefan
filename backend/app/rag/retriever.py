"""Document retrieval using embeddings and vector store."""

import logging

from app.models import Source
from app.rag.embedder import CohereEmbedder
from app.rag.vectorstore import VectorStore

logger = logging.getLogger(__name__)


def retrieve(
    question: str,
    embedder: CohereEmbedder,
    vector_store: VectorStore,
    top_k: int = 4,
) -> list[Source]:
    """Retrieve relevant document chunks for a question.

    Args:
        question: The user's question.
        embedder: Cohere embedder instance for query embedding.
        vector_store: ChromaDB vector store to search.
        top_k: Number of results to return.

    Returns:
        List of Source objects with chunk text and similarity scores.
    """
    logger.info("Retrieving for question: %s", question[:80])

    query_embedding = embedder.embed_query(question)
    results = vector_store.query(query_embedding, top_k=top_k)

    sources = []
    for chunk, score in results:
        sources.append(
            Source(
                chunk_id=chunk.chunk_id,
                source_file=chunk.metadata.get("source_file", "unknown"),
                source_type=chunk.metadata.get("source_type", "other"),
                location=chunk.metadata.get("location", "unknown"),
                text=chunk.text,
                similarity_score=score,
            )
        )

    top_score = sources[0].similarity_score if sources else 0
    logger.info("Retrieved %d sources (top score: %.3f)", len(sources), top_score)
    return sources
