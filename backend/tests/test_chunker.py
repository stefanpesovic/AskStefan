"""Tests for document chunking."""

from app.rag.chunker import Chunk, _make_chunk_id, _slugify, chunk_documents
from app.rag.loaders import Document


class TestSlugify:
    """Tests for the slugify helper."""

    def test_basic(self):
        assert _slugify("Page 1") == "page_1"

    def test_special_chars(self):
        assert _slugify("stefan cv.pdf") == "stefan_cv_pdf"

    def test_multiple_spaces(self):
        assert _slugify("section:  My Projects") == "section_my_projects"


class TestMakeChunkId:
    """Tests for chunk ID generation."""

    def test_format(self):
        cid = _make_chunk_id("cv.pdf", "page 1", 0)
        assert cid == "cv_pdf__page_1__0"

    def test_with_spaces(self):
        cid = _make_chunk_id("stefan cv.pdf", "page 2", 3)
        assert cid == "stefan_cv_pdf__page_2__3"

    def test_section_location(self):
        cid = _make_chunk_id("projects.md", "section: Experience", 1)
        assert cid == "projects_md__section_experience__1"


class TestChunkDocuments:
    """Tests for the chunk_documents function."""

    def test_basic_chunking(self):
        meta = {"source_file": "test.pdf", "location": "page 1"}
        docs = [Document(text="A" * 1000, metadata=meta)]
        chunks = chunk_documents(docs, chunk_size=500, chunk_overlap=50)
        assert len(chunks) >= 2

    def test_preserves_metadata(self):
        docs = [
            Document(
                text="Short text about skills.",
                metadata={
                    "source_file": "cv.pdf",
                    "source_type": "resume",
                    "location": "page 1",
                    "page": 1,
                },
            )
        ]
        chunks = chunk_documents(docs, chunk_size=500, chunk_overlap=50)
        assert len(chunks) == 1
        assert chunks[0].metadata["source_file"] == "cv.pdf"
        assert chunks[0].metadata["source_type"] == "resume"
        assert chunks[0].metadata["page"] == 1

    def test_adds_chunk_index(self):
        meta = {"source_file": "test.pdf", "location": "page 1"}
        docs = [Document(text="A" * 1000, metadata=meta)]
        chunks = chunk_documents(docs, chunk_size=500, chunk_overlap=50)
        indices = [c.metadata["chunk_index"] for c in chunks]
        assert indices == list(range(len(chunks)))

    def test_unique_chunk_ids(self):
        docs = [
            Document(text="A" * 600, metadata={"source_file": "cv.pdf", "location": "page 1"}),
            Document(text="B" * 600, metadata={"source_file": "cv.pdf", "location": "page 2"}),
        ]
        chunks = chunk_documents(docs, chunk_size=500, chunk_overlap=50)
        ids = [c.chunk_id for c in chunks]
        assert len(ids) == len(set(ids))

    def test_small_text_single_chunk(self):
        meta = {"source_file": "test.md", "location": "intro"}
        docs = [Document(text="Hello world", metadata=meta)]
        chunks = chunk_documents(docs, chunk_size=500, chunk_overlap=50)
        assert len(chunks) == 1
        assert chunks[0].text == "Hello world"

    def test_empty_documents_list(self):
        chunks = chunk_documents([], chunk_size=500, chunk_overlap=50)
        assert chunks == []

    def test_chunk_type(self):
        meta = {"source_file": "t.pdf", "location": "page 1"}
        docs = [Document(text="Some text", metadata=meta)]
        chunks = chunk_documents(docs)
        assert isinstance(chunks[0], Chunk)
        assert isinstance(chunks[0].chunk_id, str)
        assert isinstance(chunks[0].text, str)
