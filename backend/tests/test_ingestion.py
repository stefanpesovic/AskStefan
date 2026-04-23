"""Tests for the ingestion pipeline."""

from pathlib import Path
from unittest.mock import MagicMock

from app.rag.ingestion import _compute_file_hash, _scan_data_dir, ingest_directory

FIXTURES_DIR = Path(__file__).parent / "fixtures"


class TestComputeFileHash:
    """Tests for SHA-256 file hashing."""

    def test_deterministic(self):
        path = FIXTURES_DIR / "sample_projects.md"
        h1 = _compute_file_hash(path)
        h2 = _compute_file_hash(path)
        assert h1 == h2

    def test_hex_format(self):
        path = FIXTURES_DIR / "sample_projects.md"
        h = _compute_file_hash(path)
        assert len(h) == 64
        assert all(c in "0123456789abcdef" for c in h)

    def test_different_files_different_hashes(self):
        h1 = _compute_file_hash(FIXTURES_DIR / "sample_projects.md")
        h2 = _compute_file_hash(FIXTURES_DIR / "sample_resume.pdf")
        assert h1 != h2


class TestScanDataDir:
    """Tests for directory scanning."""

    def test_finds_supported_files(self, tmp_path: Path):
        (tmp_path / "doc.pdf").write_bytes(b"%PDF-1.4 test")
        (tmp_path / "notes.md").write_text("# Notes")
        (tmp_path / "ignore.txt").write_text("skip me")
        files = _scan_data_dir(tmp_path)
        names = [f.name for f in files]
        assert "doc.pdf" in names
        assert "notes.md" in names
        assert "ignore.txt" not in names

    def test_empty_directory(self, tmp_path: Path):
        files = _scan_data_dir(tmp_path)
        assert files == []


class TestIngestDirectory:
    """Tests for the full ingestion pipeline."""

    def _make_mocks(self, existing_hashes: set[str] | None = None):
        """Create mock embedder and vector store."""
        mock_embedder = MagicMock()
        mock_embedder.embed_texts.return_value = [[0.1] * 1024]

        mock_store = MagicMock()
        mock_store.get_file_hashes.return_value = existing_hashes or set()
        mock_store.count.return_value = 0

        return mock_embedder, mock_store

    def test_ingests_new_file(self, tmp_path: Path):
        md_file = tmp_path / "projects.md"
        md_file.write_text("## Alpha\n\nProject Alpha is great.\n")

        embedder, store = self._make_mocks()
        store.count.return_value = 1
        embedder.embed_texts.return_value = [[0.1] * 1024]

        result = ingest_directory(tmp_path, embedder, store)

        assert len(result.new_files) == 1
        assert result.new_files[0].filename == "projects.md"
        assert result.new_files[0].source_type == "project_description"
        assert len(result.skipped_files) == 0
        embedder.embed_texts.assert_called_once()
        store.add_chunks.assert_called_once()

    def test_skips_existing_hash(self, tmp_path: Path):
        md_file = tmp_path / "projects.md"
        md_file.write_text("## Alpha\n\nProject Alpha is great.\n")
        file_hash = _compute_file_hash(md_file)

        embedder, store = self._make_mocks(existing_hashes={file_hash})

        result = ingest_directory(tmp_path, embedder, store)

        assert len(result.new_files) == 0
        assert result.skipped_files == ["projects.md"]
        embedder.embed_texts.assert_not_called()
        store.add_chunks.assert_not_called()

    def test_force_reingests(self, tmp_path: Path):
        md_file = tmp_path / "projects.md"
        md_file.write_text("## Alpha\n\nProject Alpha is great.\n")
        file_hash = _compute_file_hash(md_file)

        embedder, store = self._make_mocks(existing_hashes={file_hash})
        store.get_file_hashes.return_value = {file_hash}
        store.count.return_value = 1
        embedder.embed_texts.return_value = [[0.1] * 1024]

        result = ingest_directory(tmp_path, embedder, store, force=True)

        assert len(result.new_files) == 1
        assert len(result.skipped_files) == 0
        store.delete_by_file_hash.assert_called_once_with(file_hash)
        embedder.embed_texts.assert_called_once()

    def test_empty_directory(self, tmp_path: Path):
        embedder, store = self._make_mocks()

        result = ingest_directory(tmp_path, embedder, store)

        assert result.new_files == []
        assert result.skipped_files == []

    def test_duration_ms_populated(self, tmp_path: Path):
        md_file = tmp_path / "test.md"
        md_file.write_text("## Section\n\nContent here.\n")

        embedder, store = self._make_mocks()
        store.count.return_value = 1
        embedder.embed_texts.return_value = [[0.1] * 1024]

        result = ingest_directory(tmp_path, embedder, store)

        assert result.duration_ms >= 0

    def test_file_hash_in_chunk_metadata(self, tmp_path: Path):
        md_file = tmp_path / "notes.md"
        md_file.write_text("## Intro\n\nSome content.\n")
        expected_hash = _compute_file_hash(md_file)

        embedder, store = self._make_mocks()
        store.count.return_value = 1
        embedder.embed_texts.return_value = [[0.1] * 1024]

        ingest_directory(tmp_path, embedder, store)

        call_args = store.add_chunks.call_args
        chunks = call_args[0][0]
        assert chunks[0].metadata["file_hash"] == expected_hash

    def test_multiple_files(self, tmp_path: Path):
        (tmp_path / "cv.pdf").write_bytes((FIXTURES_DIR / "sample_resume.pdf").read_bytes())
        (tmp_path / "projects.md").write_text("## Alpha\n\nProject Alpha.\n")

        embedder, store = self._make_mocks()
        store.count.return_value = 3
        embedder.embed_texts.return_value = [[0.1] * 1024] * 5

        result = ingest_directory(tmp_path, embedder, store)

        assert len(result.new_files) == 2
        filenames = [f.filename for f in result.new_files]
        assert "cv.pdf" in filenames
        assert "projects.md" in filenames
