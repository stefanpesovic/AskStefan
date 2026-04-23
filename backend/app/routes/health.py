"""Health check and welcome endpoints."""

import logging
from typing import Any

from fastapi import APIRouter, Request

from app.config import Settings

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/health")
async def health(request: Request) -> dict[str, Any]:
    """Health check with system status flags.

    Returns:
        Dict with status, version, and readiness flags.
    """
    settings: Settings = request.app.state.settings
    vector_store = request.app.state.vector_store

    chunks_count = vector_store.count() if vector_store else 0

    return {
        "status": "healthy",
        "version": Settings.VERSION,
        "vectorstore_ready": chunks_count > 0,
        "chunks_count": chunks_count,
        "cohere_configured": bool(settings.COHERE_API_KEY),
        "groq_configured": bool(settings.GROQ_API_KEY),
    }


@router.get("/")
async def root() -> dict[str, str]:
    """Welcome endpoint with link to docs.

    Returns:
        Welcome message and docs URL.
    """
    return {
        "message": "Welcome to AskStefan API",
        "docs": "/docs",
    }
