"""Tests for API endpoints."""

from pathlib import Path
from unittest.mock import MagicMock, patch

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.models import Source
from app.rag.chunker import Chunk


def _create_test_app(
    chunks_count: int = 5,
    sources: list[Source] | None = None,
    answer: str = "I have experience with Python.",
    data_dir: Path | None = None,
):
    """Create a FastAPI test app with mocked dependencies.

    Args:
        chunks_count: Number of chunks in the mock vectorstore.
        sources: Mock sources to return from retriever.
        answer: Mock answer from generator.
        data_dir: Path to data directory for ingest tests.

    Returns:
        TestClient instance.
    """
    from app.routes import chat, health, ingest

    app = FastAPI()
    app.include_router(health.router)
    app.include_router(chat.router)
    app.include_router(ingest.router)

    mock_settings = MagicMock()
    mock_settings.GROQ_API_KEY = "test_groq_key"
    mock_settings.COHERE_API_KEY = "test_cohere_key"
    mock_settings.GROQ_MODEL = "llama-3.3-70b-versatile"
    mock_settings.COHERE_MODEL = "embed-english-v3.0"
    mock_settings.TOP_K = 4
    mock_settings.CHUNK_SIZE = 500
    mock_settings.CHUNK_OVERLAP = 50
    mock_settings.LLM_TEMPERATURE = 0.1
    mock_settings.LLM_MAX_TOKENS = 500
    mock_settings.LLM_TIMEOUT_SECONDS = 15
    mock_settings.MAX_RETRIES = 3
    mock_settings.DATA_DIR = data_dir or Path("/tmp/test_data")

    mock_embedder = MagicMock()
    mock_embedder.embed_query.return_value = [0.1] * 1024
    mock_embedder.embed_texts.return_value = [[0.1] * 1024]

    mock_store = MagicMock()
    mock_store.count.return_value = chunks_count
    mock_store.list_ingested_files.return_value = []
    mock_store.get_file_hashes.return_value = set()
    mock_store.query.return_value = [
        (
            Chunk(
                chunk_id="cv_pdf__page_1__0",
                text=s.text,
                metadata={
                    "source_file": s.source_file,
                    "source_type": s.source_type,
                    "location": s.location,
                },
            ),
            s.similarity_score,
        )
        for s in (sources or [])
    ]

    app.state.settings = mock_settings
    app.state.embedder = mock_embedder
    app.state.vector_store = mock_store

    return TestClient(app), mock_embedder, mock_store, mock_settings


def _default_sources() -> list[Source]:
    return [
        Source(
            chunk_id="cv_pdf__page_1__0",
            source_file="cv.pdf",
            source_type="resume",
            location="page 1",
            text="Experienced Python developer with FastAPI skills.",
            similarity_score=0.92,
        )
    ]


class TestHealthEndpoint:
    """Tests for GET /health."""

    def test_returns_healthy(self):
        client, *_ = _create_test_app(chunks_count=10)
        resp = client.get("/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "healthy"
        assert data["vectorstore_ready"] is True
        assert data["chunks_count"] == 10
        assert data["cohere_configured"] is True
        assert data["groq_configured"] is True

    def test_empty_vectorstore(self):
        client, *_ = _create_test_app(chunks_count=0)
        resp = client.get("/health")
        data = resp.json()
        assert data["vectorstore_ready"] is False
        assert data["chunks_count"] == 0


class TestRootEndpoint:
    """Tests for GET /."""

    def test_returns_welcome(self):
        client, *_ = _create_test_app()
        resp = client.get("/")
        assert resp.status_code == 200
        data = resp.json()
        assert "AskStefan" in data["message"]
        assert data["docs"] == "/docs"


class TestChatEndpoint:
    """Tests for POST /chat."""

    @patch("app.routes.chat.generate_answer")
    @patch("app.routes.chat.retrieve")
    def test_success(self, mock_retrieve, mock_generate):
        sources = _default_sources()
        mock_retrieve.return_value = sources
        mock_generate.return_value = "I have experience with Python and FastAPI."

        client, *_ = _create_test_app(chunks_count=5, sources=sources)
        resp = client.post("/chat", json={"question": "What are your skills?"})

        assert resp.status_code == 200
        data = resp.json()
        assert "Python" in data["answer"]
        assert len(data["sources"]) == 1
        assert data["model"] == "llama-3.3-70b-versatile"
        assert data["latency_ms"] >= 0

    def test_empty_question_rejected(self):
        client, *_ = _create_test_app()
        resp = client.post("/chat", json={"question": ""})
        assert resp.status_code == 422

    def test_question_too_long_rejected(self):
        client, *_ = _create_test_app()
        resp = client.post("/chat", json={"question": "x" * 501})
        assert resp.status_code == 422

    def test_empty_vectorstore_returns_503(self):
        client, *_ = _create_test_app(chunks_count=0)
        resp = client.post("/chat", json={"question": "What skills do you have?"})
        assert resp.status_code == 503
        assert "not yet indexed" in resp.json()["detail"]

    @patch("app.routes.chat.generate_answer")
    @patch("app.routes.chat.retrieve")
    def test_groq_rate_limit_returns_429(self, mock_retrieve, mock_generate):
        from groq import RateLimitError

        mock_retrieve.return_value = _default_sources()
        mock_generate.side_effect = RateLimitError(
            message="Rate limit exceeded",
            response=MagicMock(status_code=429, headers={}),
            body=None,
        )

        client, *_ = _create_test_app(chunks_count=5)
        resp = client.post("/chat", json={"question": "Tell me about yourself"})

        assert resp.status_code == 429
        assert "Retry-After" in resp.headers

    @patch("app.routes.chat.generate_answer")
    @patch("app.routes.chat.retrieve")
    def test_response_structure(self, mock_retrieve, mock_generate):
        sources = _default_sources()
        mock_retrieve.return_value = sources
        mock_generate.return_value = "Test answer."

        client, *_ = _create_test_app(chunks_count=5)
        resp = client.post("/chat", json={"question": "Test question?"})

        data = resp.json()
        assert "answer" in data
        assert "sources" in data
        assert "latency_ms" in data
        assert "model" in data
        src = data["sources"][0]
        assert "chunk_id" in src
        assert "source_file" in src
        assert "source_type" in src
        assert "location" in src
        assert "text" in src
        assert "similarity_score" in src


class TestIngestEndpoint:
    """Tests for POST /ingest."""

    @patch("app.routes.ingest.ingest_directory")
    def test_ingest_success(self, mock_ingest, tmp_path: Path):
        from app.models import IngestResponse

        (tmp_path / "test.md").write_text("# Test\nContent")
        mock_ingest.return_value = IngestResponse(
            new_files=[],
            skipped_files=[],
            total_chunks=5,
            duration_ms=100,
        )

        client, _, _, settings = _create_test_app(data_dir=tmp_path)
        resp = client.post("/ingest")

        assert resp.status_code == 200
        data = resp.json()
        assert "new_files" in data
        assert "skipped_files" in data
        assert "total_chunks" in data

    def test_empty_data_dir_returns_404(self, tmp_path: Path):
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()
        client, *_ = _create_test_app(data_dir=empty_dir)
        resp = client.post("/ingest")
        assert resp.status_code == 404

    @patch("app.routes.ingest.ingest_directory")
    def test_ingest_idempotent(self, mock_ingest, tmp_path: Path):
        from app.models import IngestResponse

        (tmp_path / "cv.pdf").write_bytes(b"%PDF test")
        mock_ingest.return_value = IngestResponse(
            new_files=[],
            skipped_files=["cv.pdf"],
            total_chunks=5,
            duration_ms=50,
        )

        client, *_ = _create_test_app(data_dir=tmp_path)
        resp = client.post("/ingest")

        assert resp.status_code == 200
        assert resp.json()["skipped_files"] == ["cv.pdf"]

    @patch("app.routes.ingest.ingest_directory")
    def test_force_param(self, mock_ingest, tmp_path: Path):
        from app.models import IngestResponse

        (tmp_path / "cv.pdf").write_bytes(b"%PDF test")
        mock_ingest.return_value = IngestResponse(
            new_files=[],
            skipped_files=[],
            total_chunks=5,
            duration_ms=100,
        )

        client, *_ = _create_test_app(data_dir=tmp_path)
        resp = client.post("/ingest?force=true")

        assert resp.status_code == 200
        call_kwargs = mock_ingest.call_args
        assert call_kwargs[1].get("force") is True or (
            len(call_kwargs[0]) > 0 and call_kwargs[0][-1] is True
        )


class TestSourcesEndpoint:
    """Tests for GET /sources."""

    def test_returns_list(self):
        client, _, mock_store, _ = _create_test_app()
        mock_store.list_ingested_files.return_value = []
        mock_store.count.return_value = 0

        resp = client.get("/sources")

        assert resp.status_code == 200
        data = resp.json()
        assert "files" in data
        assert "total_chunks" in data
        assert isinstance(data["files"], list)
