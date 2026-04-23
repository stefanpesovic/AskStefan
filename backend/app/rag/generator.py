"""LLM answer generation via Groq with citation-aware prompting."""

import logging
import time

from groq import Groq, RateLimitError

from app.config import Settings
from app.models import Source

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "You are AskStefan, an AI assistant that answers questions about "
    "Stefan Pešović strictly based on provided document excerpts from "
    "his CV, project descriptions, and other personal documents.\n"
    "Rules:\n\n"
    "Answer ONLY using information from the provided excerpts below.\n"
    "If the excerpts don't contain enough information, say: "
    "\"I don't have that information in my documents. "
    'You can ask Stefan directly via the contact links."\n'
    "Be concise but warm. Write in first person AS IF you are Stefan "
    "speaking.\n"
    "When relevant, naturally reference the source: "
    '"According to my CV..." or "In my AIJobRadar project..."\n'
    "Never invent facts, dates, technologies, or experiences not "
    "present in the excerpts.\n"
    "If asked about personal opinions, feelings, or predictions beyond "
    "the documents, redirect: "
    "\"That's beyond what's documented. "
    'Feel free to reach out to me directly."\n\n'
    "Format: plain text, no markdown. Keep responses under 150 words "
    "unless more detail is explicitly requested."
)


def _build_user_prompt(question: str, sources: list[Source]) -> str:
    """Build the user prompt with question and source excerpts.

    Args:
        question: The user's question.
        sources: Retrieved source chunks.

    Returns:
        Formatted prompt string with excerpts.
    """
    excerpts = []
    for i, src in enumerate(sources, 1):
        excerpts.append(f"[Excerpt {i}] (from {src.source_file}, {src.location}):\n{src.text}")

    excerpts_text = "\n\n".join(excerpts)
    return f"Document excerpts:\n\n{excerpts_text}\n\nQuestion: {question}"


def generate_answer(
    question: str,
    sources: list[Source],
    settings: Settings,
) -> str:
    """Generate an answer using Groq LLM based on retrieved sources.

    Args:
        question: The user's question.
        sources: Retrieved document chunks for context.
        settings: Application settings with Groq config.

    Returns:
        Generated answer string.

    Raises:
        RateLimitError: After exhausting retries on 429.
    """
    client = Groq(api_key=settings.GROQ_API_KEY)
    user_prompt = _build_user_prompt(question, sources)

    for attempt in range(settings.MAX_RETRIES):
        try:
            start = time.monotonic()
            response = client.chat.completions.create(
                model=settings.GROQ_MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=settings.LLM_TEMPERATURE,
                max_tokens=settings.LLM_MAX_TOKENS,
                timeout=settings.LLM_TIMEOUT_SECONDS,
            )
            elapsed_ms = int((time.monotonic() - start) * 1000)
            answer = response.choices[0].message.content.strip()
            logger.info(
                "Groq generation: model=%s, %dms, %d chars",
                settings.GROQ_MODEL,
                elapsed_ms,
                len(answer),
            )
            return answer
        except RateLimitError:
            if attempt == settings.MAX_RETRIES - 1:
                logger.error("Groq rate limit exhausted after %d retries", settings.MAX_RETRIES)
                raise
            wait = 2**attempt
            logger.warning(
                "Groq 429 — retrying in %ds (attempt %d/%d)",
                wait,
                attempt + 1,
                settings.MAX_RETRIES,
            )
            time.sleep(wait)

    raise RuntimeError("Unreachable: retry loop exited without return or raise")
