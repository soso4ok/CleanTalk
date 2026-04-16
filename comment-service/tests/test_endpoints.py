import pytest
from unittest.mock import patch

def test_list_comments_empty(client):
    response = client.get("/comments?post_id=post_1")
    assert response.status_code == 200
    assert response.json() == []

@patch("app.routers.comments.moderate_comment")
def test_submit_comment_success(mock_moderate, authenticated_client):
    mock_moderate.return_value = "ok"
    
    comment_data = {"post_id": "post_1", "body": "Great post!"}
    response = authenticated_client.post("/comments", json=comment_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["verdict"] == "ok"
    assert data["body"] == "Great post!"
    assert "comment_id" in data

@patch("app.routers.comments.moderate_comment")
def test_submit_comment_spam(mock_moderate, authenticated_client):
    mock_moderate.return_value = "spam"
    
    comment_data = {"post_id": "post_1", "body": "Buy cheap meds!"}
    response = authenticated_client.post("/comments", json=comment_data)
    
    assert response.status_code == 422
    assert "spam" in response.json()["detail"]

def test_remove_comment_success(authenticated_client, db, mock_user):
    # Manually create a comment in DB
    from app.models import Comment
    comment = Comment(
        id="comm_1",
        post_id="post_1",
        author_id=mock_user.user_id,
        author_name=mock_user.username,
        body="Delete me",
        status="ok"
    )
    db.add(comment)
    db.commit()
    
    response = authenticated_client.delete("/comments/comm_1")
    assert response.status_code == 204
    
    # Verify it's gone
    assert db.query(Comment).filter(Comment.id == "comm_1").first() is None

def test_remove_comment_forbidden(authenticated_client, db):
    # Created by another user
    from app.models import Comment
    comment = Comment(
        id="comm_2",
        post_id="post_1",
        author_id="other_user",
        author_name="other",
        body="Can't delete this",
        status="ok"
    )
    db.add(comment)
    db.commit()
    
    response = authenticated_client.delete("/comments/comm_2")
    assert response.status_code == 403
