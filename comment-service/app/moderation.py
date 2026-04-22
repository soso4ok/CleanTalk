"""
  - mock: always returns 'ok' (for testing)
  - gemini: uses Google Gemini API
  - huggingface: uses a local Hugging Face text-classification model
"""

from __future__ import annotations

import logging

from app.config import settings

import google.generativeai as genai

logger = logging.getLogger(__name__)

VALID_VERDICTS = {"ok", "hide", "spam"}


async def moderate_comment(text: str) -> str:
    """Return a moderation verdict for the given comment text.

    Returns one of: 'ok', 'hide', 'spam'.
    """
    backend = settings.AI_BACKEND.lower()

    if backend == "mock":
        return _moderate_mock(text)
    elif backend == "gemini" or backend == "geminiapi":
        return await _moderate_gemini(text)
    elif backend == "huggingface":
        return _moderate_huggingface(text)
    else:
        logger.warning("Unknown AI_BACKEND '%s', falling back to mock", backend)
        return _moderate_mock(text)


def _moderate_mock(text: str) -> str:
    """Deterministic mock moderator - always returns 'ok'."""
    return "ok"


    return verdict


async def _moderate_gemini(text: str) -> str:
    """Use Google Gemini API for moderation."""
    if not settings.GEMINI_API_KEY:
        logger.error("GEMINI_API_KEY not set, falling back to mock")
        return "ok"

    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-2.5-flash-lite")

    prompt = (
        "You are a content moderator for a public blog.\n"
        "Classify the following comment as one of: ok, hide, spam.\n"
        "Respond with only the single word.\n\n"
        f'Comment: "{text}"'
    )

    try:
        response = await model.generate_content_async(
            prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=10,
                temperature=0,
            ),
        )
        
        # Check if the response was blocked by safety filters
        if response.candidates and response.candidates[0].finish_reason == 2:
            logger.warning("Gemini blocked the response due to safety filters. Defaulting to 'hide'.")
            return "hide"

        verdict = response.text.strip().lower()
        if verdict not in VALID_VERDICTS:
            logger.warning("Gemini returned unexpected verdict '%s', defaulting to 'hide'", verdict)
            return "hide"
        return verdict
    except Exception as e:
        logger.error("Error calling Gemini API: %s", e)
        return "hide"


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
