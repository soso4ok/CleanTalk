import pytest
from unittest.mock import AsyncMock, patch
from app.moderation import moderate_comment
from app.config import settings

@pytest.mark.asyncio
async def test_moderate_comment_mock_backend():
    """Test that it returns 'ok' when backend is set to mock."""
    with patch("app.moderation.settings.AI_BACKEND", "mock"):
        verdict = await moderate_comment("This is a test")
        assert verdict == "ok"

@pytest.mark.asyncio
@patch("google.generativeai.GenerativeModel.generate_content_async")
async def test_moderate_comment_gemini_success(mock_generate, monkeypatch):
    """Test successful Gemini moderation."""
    monkeypatch.setattr(settings, "AI_BACKEND", "gemini")
    monkeypatch.setattr(settings, "GEMINI_API_KEY", "fake_key")
    
    # Mock response object
    mock_response = AsyncMock()
    mock_response.text = "spam"
    mock_generate.return_value = mock_response

    verdict = await moderate_comment("Buy cheap meds!")
    assert verdict == "spam"
    mock_generate.assert_called_once()

@pytest.mark.asyncio
@patch("google.generativeai.GenerativeModel.generate_content_async")
async def test_moderate_comment_gemini_unexpected_verdict(mock_generate, monkeypatch):
    """Test that Gemini defaults to 'hide' on unexpected verdicts."""
    monkeypatch.setattr(settings, "AI_BACKEND", "gemini")
    monkeypatch.setattr(settings, "GEMINI_API_KEY", "fake_key")
    
    mock_response = AsyncMock()
    mock_response.text = "something_weird"
    mock_generate.return_value = mock_response

    verdict = await moderate_comment("Some text")
    assert verdict == "hide"

@pytest.mark.asyncio
@patch("google.generativeai.GenerativeModel.generate_content_async")
async def test_moderate_comment_gemini_failure(mock_generate, monkeypatch):
    """Test that Gemini defaults to 'hide' on API error."""
    monkeypatch.setattr(settings, "AI_BACKEND", "gemini")
    monkeypatch.setattr(settings, "GEMINI_API_KEY", "fake_key")
    
    mock_generate.side_effect = Exception("API Down")

    verdict = await moderate_comment("Some text")
    assert verdict == "hide"

@pytest.mark.asyncio
async def test_moderate_comment_gemini_missing_key(monkeypatch):
    """Test that Gemini falls back to 'ok' if key is missing."""
    monkeypatch.setattr(settings, "AI_BACKEND", "gemini")
    monkeypatch.setattr(settings, "GEMINI_API_KEY", "")
    
    verdict = await moderate_comment("Some text")
    assert verdict == "ok"
