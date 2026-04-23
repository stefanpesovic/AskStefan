"""Chat endpoint for question answering."""

import logging
import time

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from groq import RateLimitError

from app.models import ChatRequest, ChatResponse
from app.rag.generator import generate_answer
from app.rag.retriever import retrieve

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: Request, body: ChatRequest) -> ChatResponse | JSONResponse:
    """Answer a question using RAG pipeline.

    Retrieves relevant document chunks, generates an answer via Groq LLM,
    and returns the answer with supporting sources.

    Args:
        request: FastAPI request with app state.
        body: Chat request with question.

    Returns:
        ChatResponse with answer, sources, latency, and model info.

    Raises:
        HTTPException: 503 if vectorstore is empty, 429 on rate limits.
    """
    settings = request.app.state.settings
    embedder = request.app.state.embedder
    vector_store = request.app.state.vector_store

    if vector_store.count() == 0:
        raise HTTPException(
            status_code=503,
            detail="Documents not yet indexed. Run POST /ingest first.",
        )

    start = time.monotonic()

    try:
        sources = retrieve(
            question=body.question,
            embedder=embedder,
            vector_store=vector_store,
            top_k=settings.TOP_K,
        )
    except Exception as e:
        logger.error("Retrieval failed: %s", str(e))
        if "TooManyRequests" in type(e).__name__:
            return JSONResponse(
                status_code=429,
                content={"detail": "Embedding service is busy. Please try again shortly."},
                headers={"Retry-After": "10"},
            )
        raise HTTPException(status_code=500, detail="Failed to retrieve documents.")

    try:
        answer = generate_answer(
            question=body.question,
            sources=sources,
            settings=settings,
        )
    except RateLimitError:
        return JSONResponse(
            status_code=429,
            content={"detail": "LLM service is busy. Please try again shortly."},
            headers={"Retry-After": "10"},
        )
    except Exception as e:
        logger.error("Generation failed: %s", str(e))
        raise HTTPException(status_code=500, detail="Failed to generate answer.")

    elapsed_ms = int((time.monotonic() - start) * 1000)

    return ChatResponse(
        answer=answer,
        sources=sources,
        latency_ms=elapsed_ms,
        model=settings.GROQ_MODEL,
    )
