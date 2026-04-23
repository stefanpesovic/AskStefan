"""Document loaders for PDF and Markdown files."""

import logging
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from fnmatch import fnmatch
from pathlib import Path

import frontmatter
from pypdf import PdfReader

from app.models import SourceType

logger = logging.getLogger(__name__)


@dataclass
class Document:
    """A loaded document segment with text and metadata."""

    text: str
    metadata: dict = field(default_factory=dict)


def infer_source_type(filename: str) -> SourceType:
    """Infer source type from filename using pattern matching.

    Args:
        filename: The filename to classify.

    Returns:
        The inferred source type.
    """
    name = filename.lower()
    if fnmatch(name, "*cv*") or fnmatch(name, "*resume*"):
        return "resume"
    if fnmatch(name, "*project*"):
        return "project_description"
    if fnmatch(name, "blog*") or fnmatch(name, "*blog*"):
        return "blog"
    if fnmatch(name, "about*") or fnmatch(name, "*about*"):
        return "about"
    return "other"


class BaseLoader(ABC):
    """Abstract base class for document loaders."""

    @abstractmethod
    def load(self, path: Path) -> list[Document]:
        """Load a file and return a list of Documents.

        Args:
            path: Path to the file to load.

        Returns:
            List of Document objects with text and metadata.
        """


class PDFLoader(BaseLoader):
    """Loads PDF files, producing one Document per page."""

    def load(self, path: Path) -> list[Document]:
        """Load a PDF file page by page.

        Args:
            path: Path to the PDF file.

        Returns:
            List of Documents, one per page with non-empty text.
        """
        logger.info("Loading PDF: %s", path.name)
        reader = PdfReader(str(path))
        source_type = infer_source_type(path.name)
        documents = []

        for i, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            text = text.strip()
            if not text:
                continue
            documents.append(
                Document(
                    text=text,
                    metadata={
                        "source_file": path.name,
                        "source_type": source_type,
                        "page": i,
                        "location": f"page {i}",
                    },
                )
            )

        logger.info("Loaded %d pages from %s", len(documents), path.name)
        return documents


class MarkdownLoader(BaseLoader):
    """Loads Markdown files, splitting by H2 headings."""

    def load(self, path: Path) -> list[Document]:
        """Load a Markdown file, splitting content by H2 sections.

        Args:
            path: Path to the Markdown file.

        Returns:
            List of Documents, one per H2 section.
        """
        logger.info("Loading Markdown: %s", path.name)
        raw = path.read_text(encoding="utf-8")
        post = frontmatter.loads(raw)
        content = post.content
        source_type = infer_source_type(path.name)

        sections = self._split_by_h2(content)
        documents = []

        for section_title, section_text in sections:
            text = section_text.strip()
            if not text:
                continue
            location = f"section: {section_title}" if section_title else "introduction"
            documents.append(
                Document(
                    text=text,
                    metadata={
                        "source_file": path.name,
                        "source_type": source_type,
                        "section": section_title or "introduction",
                        "location": location,
                    },
                )
            )

        logger.info("Loaded %d sections from %s", len(documents), path.name)
        return documents

    def _split_by_h2(self, content: str) -> list[tuple[str, str]]:
        """Split markdown content by H2 headings.

        Args:
            content: Raw markdown text.

        Returns:
            List of (heading_title, section_text) tuples.
        """
        pattern = re.compile(r"^## (.+)$", re.MULTILINE)
        matches = list(pattern.finditer(content))

        if not matches:
            return [("", content)]

        sections = []

        # Content before first H2
        pre_heading = content[: matches[0].start()].strip()
        if pre_heading:
            sections.append(("", pre_heading))

        for i, match in enumerate(matches):
            title = match.group(1).strip()
            start = match.end()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
            sections.append((title, content[start:end]))

        return sections


_LOADERS: dict[str, BaseLoader] = {
    ".pdf": PDFLoader(),
    ".md": MarkdownLoader(),
}

SUPPORTED_EXTENSIONS = set(_LOADERS.keys())


def load_document(path: Path) -> list[Document]:
    """Load a document using the appropriate loader based on file extension.

    Args:
        path: Path to the document file.

    Returns:
        List of Documents from the file.

    Raises:
        ValueError: If the file extension is not supported.
    """
    ext = path.suffix.lower()
    loader = _LOADERS.get(ext)
    if loader is None:
        raise ValueError(f"Unsupported file extension: {ext}. Supported: {SUPPORTED_EXTENSIONS}")
    return loader.load(path)
