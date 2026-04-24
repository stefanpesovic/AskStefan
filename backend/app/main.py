"""FastAPI application entry point with lifespan management."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import Settings, get_settings
from app.rag.embedder import CohereEmbedder
from app.rag.vectorstore import VectorStore
from app.routes import chat, health, ingest

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize resources on startup and clean up on shutdown."""
    settings = get_settings()

    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    logger.info("Starting AskStefan API v%s", Settings.VERSION)

    app.state.settings = settings
    app.state.embedder = CohereEmbedder.get_instance(settings)
    app.state.vector_store = VectorStore(settings.CHROMA_PERSIST_DIR)

    chunks = app.state.vector_store.count()
    logger.info("Resources initialized — vectorstore has %d chunks", chunks)

    yield

    CohereEmbedder.reset()
    logger.info("AskStefan API shutdown complete")


app = FastAPI(
    title="AskStefan API",
    description="RAG chatbot API for answering questions about Stefan Pešović",
    version=Settings.VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_settings().cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, tags=["Health"])
app.include_router(chat.router, tags=["Chat"])
app.include_router(ingest.router, tags=["Ingestion"])
