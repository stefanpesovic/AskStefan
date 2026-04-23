"""Pydantic schemas for API requests and responses."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

SourceType = Literal["resume", "project_description", "blog", "about", "other"]


class ChatRequest(BaseModel):
    """Incoming chat question."""

    question: str = Field(min_length=1, max_length=500)


class Source(BaseModel):
    """A retrieved document chunk with similarity score."""

    chunk_id: str
    source_file: str
    source_type: SourceType
    location: str
    text: str
    similarity_score: float


class ChatResponse(BaseModel):
    """Chat answer with supporting sources."""

    answer: str
    sources: list[Source]
    latency_ms: int
    model: str


class IngestedFile(BaseModel):
    """Metadata about a single ingested file."""

    filename: str
    source_type: SourceType
    chunks_created: int
    file_hash: str
    ingested_at: datetime


class IngestResponse(BaseModel):
    """Result of an ingestion run."""

    new_files: list[IngestedFile]
    skipped_files: list[str]
    total_chunks: int
    duration_ms: int


class SourcesListResponse(BaseModel):
    """List of all ingested files."""

    files: list[IngestedFile]
    total_chunks: int
