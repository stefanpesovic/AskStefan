"""Tests for document loaders."""

from pathlib import Path

import pytest

from app.rag.loaders import (
    MarkdownLoader,
    PDFLoader,
    infer_source_type,
    load_document,
)


class TestInferSourceType:
    """Tests for source type inference from filenames."""

    def test_cv_in_filename(self):
        assert infer_source_type("stefan cv.pdf") == "resume"

    def test_cv_exact(self):
        assert infer_source_type("cv.pdf") == "resume"

    def test_resume_in_filename(self):
        assert infer_source_type("my_resume_2024.pdf") == "resume"

    def test_project_in_filename(self):
        assert infer_source_type("projects.md") == "project_description"

    def test_project_partial_match(self):
        assert infer_source_type("cool_project_details.md") == "project_description"

    def test_blog_prefix(self):
        assert infer_source_type("blog_post_1.md") == "blog"

    def test_about_prefix(self):
        assert infer_source_type("about_me.md") == "about"

    def test_unknown_defaults_to_other(self):
        assert infer_source_type("notes.md") == "other"

    def test_case_insensitive(self):
        assert infer_source_type("MY_CV.PDF") == "resume"


class TestPDFLoader:
    """Tests for PDF document loading."""

    def test_loads_pages(self, sample_resume_pdf: Path):
        loader = PDFLoader()
        docs = loader.load(sample_resume_pdf)
        assert len(docs) == 2

    def test_page_metadata(self, sample_resume_pdf: Path):
        loader = PDFLoader()
        docs = loader.load(sample_resume_pdf)
        assert docs[0].metadata["page"] == 1
        assert docs[0].metadata["location"] == "page 1"
        assert docs[1].metadata["page"] == 2
        assert docs[1].metadata["location"] == "page 2"

    def test_source_file_in_metadata(self, sample_resume_pdf: Path):
        loader = PDFLoader()
        docs = loader.load(sample_resume_pdf)
        assert docs[0].metadata["source_file"] == "sample_resume.pdf"

    def test_source_type_inferred(self, sample_resume_pdf: Path):
        loader = PDFLoader()
        docs = loader.load(sample_resume_pdf)
        assert docs[0].metadata["source_type"] == "resume"

    def test_text_not_empty(self, sample_resume_pdf: Path):
        loader = PDFLoader()
        docs = loader.load(sample_resume_pdf)
        for doc in docs:
            assert len(doc.text) > 0


class TestMarkdownLoader:
    """Tests for Markdown document loading."""

    def test_loads_sections(self, sample_projects_md: Path):
        loader = MarkdownLoader()
        docs = loader.load(sample_projects_md)
        # intro + H1 content before first H2, then 3 H2 sections
        assert len(docs) >= 3

    def test_section_metadata(self, sample_projects_md: Path):
        loader = MarkdownLoader()
        docs = loader.load(sample_projects_md)
        sections = [d.metadata.get("section") for d in docs]
        assert "Project Alpha" in sections
        assert "Project Beta" in sections

    def test_location_format(self, sample_projects_md: Path):
        loader = MarkdownLoader()
        docs = loader.load(sample_projects_md)
        alpha_doc = [d for d in docs if d.metadata.get("section") == "Project Alpha"][0]
        assert alpha_doc.metadata["location"] == "section: Project Alpha"

    def test_source_type_inferred(self, sample_projects_md: Path):
        loader = MarkdownLoader()
        docs = loader.load(sample_projects_md)
        assert docs[0].metadata["source_type"] == "project_description"

    def test_source_file_in_metadata(self, sample_projects_md: Path):
        loader = MarkdownLoader()
        docs = loader.load(sample_projects_md)
        assert docs[0].metadata["source_file"] == "sample_projects.md"

    def test_frontmatter_stripped(self, sample_projects_md: Path):
        loader = MarkdownLoader()
        docs = loader.load(sample_projects_md)
        for doc in docs:
            assert "---" not in doc.text or "title:" not in doc.text


class TestLoadDocument:
    """Tests for the dispatcher function."""

    def test_pdf_dispatch(self, sample_resume_pdf: Path):
        docs = load_document(sample_resume_pdf)
        assert len(docs) > 0

    def test_markdown_dispatch(self, sample_projects_md: Path):
        docs = load_document(sample_projects_md)
        assert len(docs) > 0

    def test_unsupported_extension(self, tmp_path: Path):
        txt_file = tmp_path / "notes.txt"
        txt_file.write_text("some text")
        with pytest.raises(ValueError, match="Unsupported file extension"):
            load_document(txt_file)
