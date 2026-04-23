"""ChromaDB vector store abstraction."""

import logging
from datetime import datetime, timezone
from pathlib import Path

import chromadb

from app.models import IngestedFile
from app.rag.chunker import Chunk

logger = logging.getLogger(__name__)

COLLECTION_NAME = "askstefan_docs"


class VectorStore:
    """Wrapper around ChromaDB for document chunk storage and retrieval.

    Args:
        persist_dir: Directory for ChromaDB persistent storage.
    """

    def __init__(self, persist_dir: Path) -> None:
        self._client = chromadb.PersistentClient(path=str(persist_dir))
        self._collection = self._client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )
        logger.info(
            "VectorStore initialized at %s (collection: %s, %d chunks)",
            persist_dir,
            COLLECTION_NAME,
            self._collection.count(),
        )

    def add_chunks(self, chunks: list[Chunk], embeddings: list[list[float]]) -> None:
        """Add chunks with their embeddings to the vector store.

        Deduplicates by chunk_id — existing IDs are skipped.

        Args:
            chunks: List of text chunks with metadata.
            embeddings: Corresponding embedding vectors.
        """
        if not chunks:
            return

        existing_ids = set(self._collection.get()["ids"])
        new_chunks = []
        new_embeddings = []

        for chunk, embedding in zip(chunks, embeddings):
            if chunk.chunk_id not in existing_ids:
                new_chunks.append(chunk)
                new_embeddings.append(embedding)

        if not new_chunks:
            logger.info("No new chunks to add (all %d already exist)", len(chunks))
            return

        self._collection.add(
            ids=[c.chunk_id for c in new_chunks],
            documents=[c.text for c in new_chunks],
            embeddings=new_embeddings,
            metadatas=[c.metadata for c in new_chunks],
        )
        skipped = len(chunks) - len(new_chunks)
        logger.info("Added %d new chunks (%d skipped)", len(new_chunks), skipped)

    def query(self, embedding: list[float], top_k: int = 4) -> list[tuple[Chunk, float]]:
        """Query the vector store for similar chunks.

        Args:
            embedding: Query embedding vector.
            top_k: Number of results to return.

        Returns:
            List of (Chunk, similarity_score) tuples, sorted by relevance.
        """
        count = self._collection.count()
        if count == 0:
            return []

        results = self._collection.query(
            query_embeddings=[embedding],
            n_results=min(top_k, count),
            include=["documents", "metadatas", "distances"],
        )

        pairs: list[tuple[Chunk, float]] = []
        for i in range(len(results["ids"][0])):
            chunk = Chunk(
                chunk_id=results["ids"][0][i],
                text=results["documents"][0][i],
                metadata=results["metadatas"][0][i],
            )
            # ChromaDB cosine distance → similarity = 1 - distance
            distance = results["distances"][0][i]
            similarity = round(1.0 - distance, 4)
            pairs.append((chunk, similarity))

        return pairs

    def get_file_hashes(self) -> set[str]:
        """Get all unique file hashes currently in the store.

        Returns:
            Set of SHA-256 hashes of ingested files.
        """
        all_meta = self._collection.get(include=["metadatas"])
        hashes: set[str] = set()
        for meta in all_meta["metadatas"]:
            if "file_hash" in meta:
                hashes.add(meta["file_hash"])
        return hashes

    def list_ingested_files(self) -> list[IngestedFile]:
        """List all ingested files with metadata.

        Returns:
            List of IngestedFile objects with aggregated chunk counts.
        """
        all_meta = self._collection.get(include=["metadatas"])
        file_map: dict[str, dict] = {}

        for meta in all_meta["metadatas"]:
            filename = meta.get("source_file", "unknown")
            if filename not in file_map:
                file_map[filename] = {
                    "filename": filename,
                    "source_type": meta.get("source_type", "other"),
                    "chunks_created": 0,
                    "file_hash": meta.get("file_hash", ""),
                    "ingested_at": meta.get("ingested_at", datetime.now(timezone.utc).isoformat()),
                }
            file_map[filename]["chunks_created"] += 1

        return [IngestedFile(**data) for data in file_map.values()]

    def count(self) -> int:
        """Return the total number of chunks in the store."""
        return self._collection.count()

    def delete_by_file_hash(self, file_hash: str) -> None:
        """Delete all chunks associated with a file hash.

        Args:
            file_hash: SHA-256 hash of the file to remove.
        """
        self._collection.delete(where={"file_hash": file_hash})
        logger.info("Deleted chunks with file_hash=%s", file_hash)
