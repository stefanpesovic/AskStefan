"""Document ingestion orchestrator: scan → load → chunk → embed → store."""

import hashlib
import logging
import time
from datetime import datetime, timezone
from pathlib import Path

from app.models import IngestedFile, IngestResponse
from app.rag.chunker import chunk_documents
from app.rag.embedder import CohereEmbedder
from app.rag.loaders import SUPPORTED_EXTENSIONS, infer_source_type, load_document
from app.rag.vectorstore import VectorStore

logger = logging.getLogger(__name__)


def _compute_file_hash(path: Path) -> str:
    """Compute SHA-256 hash of a file.

    Args:
        path: Path to the file.

    Returns:
        Hex-encoded SHA-256 hash string.
    """
    sha256 = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(8192), b""):
            sha256.update(block)
    return sha256.hexdigest()


def _scan_data_dir(data_dir: Path) -> list[Path]:
    """Scan directory for supported document files.

    Args:
        data_dir: Directory to scan.

    Returns:
        Sorted list of paths to supported files.
    """
    files = []
    for ext in SUPPORTED_EXTENSIONS:
        files.extend(data_dir.glob(f"*{ext}"))
    return sorted(set(files))


def ingest_directory(
    data_dir: Path,
    embedder: CohereEmbedder,
    vector_store: VectorStore,
    chunk_size: int = 500,
    chunk_overlap: int = 50,
    force: bool = False,
) -> IngestResponse:
    """Ingest all supported documents from a directory.

    Computes SHA-256 of each file. Skips files whose hash already exists
    in the vector store unless force=True.

    Args:
        data_dir: Directory containing documents.
        embedder: Cohere embedder for generating vectors.
        vector_store: ChromaDB store for persisting chunks.
        chunk_size: Maximum characters per chunk.
        chunk_overlap: Character overlap between chunks.
        force: If True, reingest all files regardless of hash.

    Returns:
        IngestResponse with stats about the ingestion run.
    """
    start = time.monotonic()
    files = _scan_data_dir(data_dir)

    if not files:
        logger.warning("No supported documents found in %s", data_dir)
        return IngestResponse(
            new_files=[],
            skipped_files=[],
            total_chunks=vector_store.count(),
            duration_ms=0,
        )

    existing_hashes = set() if force else vector_store.get_file_hashes()
    new_files: list[IngestedFile] = []
    skipped_files: list[str] = []

    for file_path in files:
        file_hash = _compute_file_hash(file_path)

        if not force and file_hash in existing_hashes:
            logger.info("Skipping %s (hash unchanged)", file_path.name)
            skipped_files.append(file_path.name)
            continue

        if force and file_hash in vector_store.get_file_hashes():
            vector_store.delete_by_file_hash(file_hash)

        logger.info("Ingesting %s", file_path.name)

        documents = load_document(file_path)
        chunks = chunk_documents(documents, chunk_size=chunk_size, chunk_overlap=chunk_overlap)

        now = datetime.now(timezone.utc).isoformat()
        for chunk in chunks:
            chunk.metadata["file_hash"] = file_hash
            chunk.metadata["ingested_at"] = now

        embeddings = embedder.embed_texts([c.text for c in chunks])
        vector_store.add_chunks(chunks, embeddings)

        new_files.append(
            IngestedFile(
                filename=file_path.name,
                source_type=infer_source_type(file_path.name),
                chunks_created=len(chunks),
                file_hash=file_hash,
                ingested_at=datetime.now(timezone.utc),
            )
        )

    elapsed_ms = int((time.monotonic() - start) * 1000)
    total_chunks = vector_store.count()

    logger.info(
        "Ingestion complete: %d new, %d skipped, %d total chunks, %dms",
        len(new_files),
        len(skipped_files),
        total_chunks,
        elapsed_ms,
    )

    return IngestResponse(
        new_files=new_files,
        skipped_files=skipped_files,
        total_chunks=total_chunks,
        duration_ms=elapsed_ms,
    )
