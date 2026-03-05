"""AI moderation module.

Supports three backends configured via AI_BACKEND env var:
  - mock: always returns 'ok' (for testing)
  - openai: uses OpenAI Chat Completions API
  - huggingface: uses a local Hugging Face text-classification model
"""

from __future__ import annotations

import logging

from app.config import settings

logger = logging.getLogger(__name__)

VALID_VERDICTS = {"ok", "hide", "spam"}


async def moderate_comment(text: str) -> str:
    """Return a moderation verdict for the given comment text.

    Returns one of: 'ok', 'hide', 'spam'.
    """
    backend = settings.AI_BACKEND.lower()

    if backend == "mock":
        return _moderate_mock(text)
    elif backend == "openai":
        return await _moderate_openai(text)
    elif backend == "huggingface":
        return _moderate_huggingface(text)
    else:
        logger.warning("Unknown AI_BACKEND '%s', falling back to mock", backend)
        return _moderate_mock(text)


def _moderate_mock(text: str) -> str:
    """Deterministic mock moderator - always returns 'ok'."""
    return "ok"


async def _moderate_openai(text: str) -> str:
    """Use OpenAI Chat Completions API for moderation."""
    from openai import AsyncOpenAI

    if not settings.OPENAI_API_KEY:
        logger.error("OPENAI_API_KEY not set, falling back to mock")
        return "ok"

    client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    prompt = (
        "You are a content moderator for a public blog.\n"
        "Classify the following comment as one of: ok, hide, spam.\n"
        "Respond with only the single word.\n\n"
        f'Comment: "{text}"'
    )

    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=10,
        temperature=0,
    )

    verdict = response.choices[0].message.content.strip().lower()
    if verdict not in VALID_VERDICTS:
        logger.warning("OpenAI returned unexpected verdict '%s', defaulting to 'hide'", verdict)
        return "hide"
    return verdict


def _moderate_huggingface(text: str) -> str:
    """Use a local Hugging Face text-classification model for moderation."""
    try:
        from transformers import pipeline
    except ImportError:
        logger.error("transformers not installed, falling back to mock")
        return "ok"

    classifier = pipeline("text-classification", model=settings.HF_MODEL_NAME)
    results = classifier(text)

    if not results:
        return "ok"

    label = results[0]["label"].lower()
    score = results[0]["score"]

    if "toxic" in label or "spam" in label:
        return "spam" if score > 0.9 else "hide"
    return "ok"
