"""Cohere embedding wrapper with rate limit handling."""

import logging
import time

import cohere

from app.config import Settings

logger = logging.getLogger(__name__)


class CohereEmbedder:
    """Singleton wrapper around Cohere's embedding API.

    Args:
        settings: Application settings with Cohere API key and model config.
    """

    _instance: "CohereEmbedder | None" = None

    def __init__(self, settings: Settings) -> None:
        self._client = cohere.Client(api_key=settings.COHERE_API_KEY)
        self._model = settings.COHERE_MODEL
        self._max_retries = settings.MAX_RETRIES

    @classmethod
    def get_instance(cls, settings: Settings) -> "CohereEmbedder":
        """Return or create the singleton embedder instance.

        Args:
            settings: Application settings.

        Returns:
            The singleton CohereEmbedder instance.
        """
        if cls._instance is None:
            cls._instance = cls(settings)
            logger.info("CohereEmbedder initialized with model=%s", settings.COHERE_MODEL)
        return cls._instance

    @classmethod
    def reset(cls) -> None:
        """Reset the singleton instance (used in testing)."""
        cls._instance = None

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """Embed a batch of texts for document storage.

        Args:
            texts: List of text strings to embed.

        Returns:
            List of embedding vectors (1024-dim each).

        Raises:
            cohere.errors.TooManyRequestsError: After exhausting retries on 429.
        """
        return self._embed(texts, input_type="search_document")

    def embed_query(self, text: str) -> list[float]:
        """Embed a single query for retrieval.

        Args:
            text: The query string to embed.

        Returns:
            A single embedding vector (1024-dim).

        Raises:
            cohere.errors.TooManyRequestsError: After exhausting retries on 429.
        """
        result = self._embed([text], input_type="search_query")
        return result[0]

    def _embed(self, texts: list[str], input_type: str) -> list[list[float]]:
        """Call Cohere embed API with exponential backoff on rate limits.

        Args:
            texts: Texts to embed.
            input_type: Either "search_document" or "search_query".

        Returns:
            List of embedding vectors.
        """
        for attempt in range(self._max_retries):
            try:
                start = time.monotonic()
                response = self._client.embed(
                    texts=texts,
                    model=self._model,
                    input_type=input_type,
                )
                elapsed_ms = int((time.monotonic() - start) * 1000)
                logger.info(
                    "Cohere embed: %d texts, input_type=%s, %dms",
                    len(texts),
                    input_type,
                    elapsed_ms,
                )
                return response.embeddings
            except cohere.TooManyRequestsError:
                if attempt == self._max_retries - 1:
                    logger.error("Cohere rate limit exhausted after %d retries", self._max_retries)
                    raise
                wait = 2**attempt
                logger.warning(
                    "Cohere 429 — retrying in %ds (attempt %d/%d)",
                    wait,
                    attempt + 1,
                    self._max_retries,
                )
                time.sleep(wait)

        raise RuntimeError("Unreachable: retry loop exited without return or raise")
