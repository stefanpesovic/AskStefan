"""Document chunking using LangChain text splitters."""

import logging
import re
from dataclasses import dataclass, field

from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.rag.loaders import Document

logger = logging.getLogger(__name__)


@dataclass
class Chunk:
    """A text chunk with metadata and unique identifier."""

    chunk_id: str
    text: str
    metadata: dict = field(default_factory=dict)


def _slugify(text: str) -> str:
    """Convert text to a URL-safe slug.

    Args:
        text: Text to slugify.

    Returns:
        Lowercase slug with only alphanumeric chars and underscores.
    """
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_")


def _make_chunk_id(source_file: str, location: str, index: int) -> str:
    """Generate a unique chunk ID.

    Args:
        source_file: Name of the source file.
        location: Location within the source (page number, section name).
        index: Chunk index within the location.

    Returns:
        Chunk ID in format: source_file__location_slug__index
    """
    file_slug = _slugify(source_file)
    loc_slug = _slugify(location)
    return f"{file_slug}__{loc_slug}__{index}"


def chunk_documents(
    documents: list[Document],
    chunk_size: int = 500,
    chunk_overlap: int = 50,
) -> list[Chunk]:
    """Split documents into chunks preserving metadata.

    Args:
        documents: List of Documents to chunk.
        chunk_size: Maximum characters per chunk.
        chunk_overlap: Character overlap between consecutive chunks.

    Returns:
        List of Chunks with unique IDs and preserved metadata.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    chunks: list[Chunk] = []

    for doc in documents:
        texts = splitter.split_text(doc.text)
        location = doc.metadata.get("location", "unknown")
        source_file = doc.metadata.get("source_file", "unknown")

        for i, text in enumerate(texts):
            chunk_id = _make_chunk_id(source_file, location, i)
            chunk_metadata = {**doc.metadata, "chunk_index": i}
            chunks.append(Chunk(chunk_id=chunk_id, text=text, metadata=chunk_metadata))

    logger.info("Created %d chunks from %d documents", len(chunks), len(documents))
    return chunks
