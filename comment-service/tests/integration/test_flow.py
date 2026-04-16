import pytest
from unittest.mock import patch, AsyncMock
from app.models import Comment

@pytest.mark.asyncio
async def test_posting_comment_integration_flow(authenticated_client, db, monkeypatch):
    """
    Test the full flow:
    1. Post a comment to the endpoint.
    2. Mock AI moderation response.
    3. Verify response status and DB state in real PostgreSQL.
    """
    # 1. Setup Mock for Gemini
    # We mock _moderate_gemini directly to simulate the integration with the rest of the app
    with patch("app.moderation._moderate_gemini", new_callable=AsyncMock) as mock_gemini:
        mock_gemini.return_value = "spam"
        
        # Configure app to use gemini backend
        from app.config import settings
        monkeypatch.setattr(settings, "AI_BACKEND", "gemini")
        monkeypatch.setattr(settings, "GEMINI_API_KEY", "test_key")

        # 2. Trigger the flow
        comment_payload = {
            "post_id": "test_post_999",
            "body": "This is a spammy comment with luxury watches."
        }
        
        # Send request
        response = authenticated_client.post("/comments", json=comment_payload)
        
        # 3. Assertions
        # For 'spam', the router raises 422
        assert response.status_code == 422
        assert "spam" in response.json()["detail"].lower()
        
        # Verify AI was called
        mock_gemini.assert_called_once_with(comment_payload["body"])
        
        # Verify NOTHING was saved in DB for spam (based on routers/comments.py logic)
        comment_in_db = db.query(Comment).filter(Comment.post_id == "test_post_999").first()
        assert comment_in_db is None

@pytest.mark.asyncio
async def test_posting_comment_approved_flow(authenticated_client, db, monkeypatch):
    """Verify that 'ok' verdict results in a 201 and 'ok' status in DB."""
    with patch("app.moderation._moderate_gemini", new_callable=AsyncMock) as mock_gemini:
        mock_gemini.return_value = "ok"
        
        from app.config import settings
        monkeypatch.setattr(settings, "AI_BACKEND", "gemini")
        monkeypatch.setattr(settings, "GEMINI_API_KEY", "test_key")

        comment_payload = {
            "post_id": "test_post_100",
            "body": "This is a very helpful comment."
        }
        
        response = authenticated_client.post("/comments", json=comment_payload)
        
        assert response.status_code == 201
        data = response.json()
        assert data["verdict"] == "ok"
        
        # Verify DB Persistence
        comment_id = data["comment_id"]
        comment_in_db = db.query(Comment).filter(Comment.id == comment_id).first()
        assert comment_in_db is not None
        assert comment_in_db.status == "ok"
        assert comment_in_db.body == comment_payload["body"]
        assert comment_in_db.post_id == comment_payload["post_id"]
