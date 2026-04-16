import pytest
from app.models import Post

def test_list_posts_empty(client):
    response = client.get("/posts")
    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []
    assert data["total"] == 0

def test_create_post(authenticated_client, mock_user):
    post_data = {"title": "New Post", "body": "Content of the post"}
    response = authenticated_client.post("/posts", json=post_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "New Post"
    assert data["author_id"] == mock_user.user_id

def test_read_post(client, db):
    post = Post(
        id="post_1",
        title="Existing Post",
        body="Some content",
        author_id="user_1",
        author_name="author1"
    )
    db.add(post)
    db.commit()
    
    response = client.get("/posts/post_1")
    assert response.status_code == 200
    assert response.json()["title"] == "Existing Post"

def test_update_post_success(authenticated_client, db, mock_user):
    post = Post(
        id="post_2",
        title="Old Title",
        body="Old body",
        author_id=mock_user.user_id,
        author_name=mock_user.username
    )
    db.add(post)
    db.commit()
    
    update_data = {"title": "New Title"}
    response = authenticated_client.put("/posts/post_2", json=update_data)
    
    assert response.status_code == 200
    assert response.json()["title"] == "New Title"

def test_update_post_forbidden(authenticated_client, db):
    post = Post(
        id="post_3",
        title="Someone else's post",
        body="Body",
        author_id="other_user",
        author_name="other"
    )
    db.add(post)
    db.commit()
    
    update_data = {"title": "Hacked Title"}
    response = authenticated_client.put("/posts/post_3", json=update_data)
    assert response.status_code == 403

def test_delete_post_success(authenticated_client, db, mock_user):
    post = Post(
        id="post_4",
        title="Delete me",
        body="Body",
        author_id=mock_user.user_id,
        author_name=mock_user.username
    )
    db.add(post)
    db.commit()
    
    response = authenticated_client.delete("/posts/post_4")
    assert response.status_code == 204
    assert db.query(Post).filter(Post.id == "post_4").first() is None
