"""Shared test fixtures."""

from pathlib import Path

import pytest

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def fixtures_dir() -> Path:
    """Return path to test fixtures directory."""
    return FIXTURES_DIR


@pytest.fixture
def sample_projects_md(fixtures_dir: Path) -> Path:
    """Return path to sample projects Markdown file."""
    return fixtures_dir / "sample_projects.md"


@pytest.fixture
def sample_resume_pdf(fixtures_dir: Path) -> Path:
    """Return path to sample resume PDF file."""
    return fixtures_dir / "sample_resume.pdf"
