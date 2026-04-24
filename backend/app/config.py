"""Application configuration via environment variables."""

from pathlib import Path
from typing import ClassVar

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """AskStefan backend configuration."""

    GROQ_API_KEY: str
    COHERE_API_KEY: str

    GROQ_MODEL: str = "llama-3.3-70b-versatile"
    COHERE_MODEL: str = "embed-english-v3.0"

    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 50
    TOP_K: int = 4

    CHROMA_PERSIST_DIR: Path = Path("chroma_db")
    DATA_DIR: Path = Path("data")

    LLM_TIMEOUT_SECONDS: int = 15
    LLM_TEMPERATURE: float = 0.1
    LLM_MAX_TOKENS: int = 500
    MAX_RETRIES: int = 3

    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173"

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    LOG_LEVEL: str = "INFO"

    VERSION: ClassVar[str] = "1.0.0"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


def get_settings() -> Settings:
    """Return cached settings instance."""
    return Settings()
