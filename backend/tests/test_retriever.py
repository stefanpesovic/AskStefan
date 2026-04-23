"""Tests for the retriever module."""

from unittest.mock import MagicMock

from app.rag.chunker import Chunk
from app.rag.retriever import retrieve


class TestRetrieve:
    """Tests for the retrieve function."""

    def _make_mocks(self, results: list[tuple[Chunk, float]]):
        """Create mock embedder and vector store.

        Args:
            results: List of (Chunk, score) tuples the mock store should return.

        Returns:
            Tuple of (mock_embedder, mock_store).
        """
        mock_embedder = MagicMock()
        mock_embedder.embed_query.return_value = [0.1] * 1024

        mock_store = MagicMock()
        mock_store.query.return_value = results

        return mock_embedder, mock_store

    def test_returns_sources(self):
        chunks = [
            (
                Chunk(
                    chunk_id="cv_pdf__page_1__0",
                    text="Python developer with 5 years experience",
                    metadata={
                        "source_file": "cv.pdf",
                        "source_type": "resume",
                        "location": "page 1",
                    },
                ),
                0.92,
            ),
            (
                Chunk(
                    chunk_id="cv_pdf__page_2__0",
                    text="Led a team of 5 engineers",
                    metadata={
                        "source_file": "cv.pdf",
                        "source_type": "resume",
                        "location": "page 2",
                    },
                ),
                0.85,
            ),
        ]
        embedder, store = self._make_mocks(chunks)

        sources = retrieve("What are your skills?", embedder, store, top_k=4)

        assert len(sources) == 2
        embedder.embed_query.assert_called_once_with("What are your skills?")
        store.query.assert_called_once()

    def test_source_fields(self):
        chunks = [
            (
                Chunk(
                    chunk_id="projects_md__section_alpha__0",
                    text="Project Alpha is a web app",
                    metadata={
                        "source_file": "projects.md",
                        "source_type": "project_description",
                        "location": "section: Project Alpha",
                    },
                ),
                0.88,
            ),
        ]
        embedder, store = self._make_mocks(chunks)

        sources = retrieve("Tell me about projects", embedder, store)

        s = sources[0]
        assert s.chunk_id == "projects_md__section_alpha__0"
        assert s.source_file == "projects.md"
        assert s.source_type == "project_description"
        assert s.location == "section: Project Alpha"
        assert s.text == "Project Alpha is a web app"
        assert s.similarity_score == 0.88

    def test_empty_results(self):
        embedder, store = self._make_mocks([])

        sources = retrieve("Unknown question", embedder, store)

        assert sources == []

    def test_respects_top_k(self):
        chunks = [
            (
                Chunk(
                    chunk_id=f"cv_pdf__page_1__{i}",
                    text=f"Chunk {i}",
                    metadata={
                        "source_file": "cv.pdf",
                        "source_type": "resume",
                        "location": "page 1",
                    },
                ),
                0.9 - i * 0.1,
            )
            for i in range(3)
        ]
        embedder, store = self._make_mocks(chunks)

        retrieve("question", embedder, store, top_k=2)

        store.query.assert_called_once_with([0.1] * 1024, top_k=2)

    def test_missing_metadata_defaults(self):
        chunks = [
            (
                Chunk(chunk_id="unknown__unknown__0", text="Some text", metadata={}),
                0.75,
            ),
        ]
        embedder, store = self._make_mocks(chunks)

        sources = retrieve("question", embedder, store)

        assert sources[0].source_file == "unknown"
        assert sources[0].source_type == "other"
        assert sources[0].location == "unknown"
