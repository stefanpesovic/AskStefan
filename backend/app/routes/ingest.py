"""Ingestion and source listing endpoints."""

import logging

from fastapi import APIRouter, HTTPException, Request

from app.models import IngestResponse, SourcesListResponse
from app.rag.ingestion import ingest_directory

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/ingest", response_model=IngestResponse)
async def ingest(request: Request, force: bool = False) -> IngestResponse:
    """Ingest documents from the data directory.

    Args:
        request: FastAPI request with app state.
        force: If True, reingest all files regardless of hash.

    Returns:
        IngestResponse with ingestion stats.

    Raises:
        HTTPException: 404 if no documents found in data directory.
    """
    settings = request.app.state.settings
    embedder = request.app.state.embedder
    vector_store = request.app.state.vector_store
    data_dir = settings.DATA_DIR

    if not data_dir.exists() or not any(data_dir.iterdir()):
        raise HTTPException(status_code=404, detail="No documents found in data/")

    result = ingest_directory(
        data_dir=data_dir,
        embedder=embedder,
        vector_store=vector_store,
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
        force=force,
    )

    logger.info(
        "Ingest complete: %d new, %d skipped",
        len(result.new_files),
        len(result.skipped_files),
    )
    return result


@router.get("/sources", response_model=SourcesListResponse)
async def list_sources(request: Request) -> SourcesListResponse:
    """List all ingested files with metadata.

    Returns:
        SourcesListResponse with file list and total chunk count.
    """
    vector_store = request.app.state.vector_store
    files = vector_store.list_ingested_files()
    total = vector_store.count()

    return SourcesListResponse(files=files, total_chunks=total)
