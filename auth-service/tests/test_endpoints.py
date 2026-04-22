import pytest
from fastapi import status

def test_register_user_success(client):
    response = client.post(
        "/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "strongpassword"
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_register_duplicate_username(client):
    # Register first user
    client.post(
        "/register",
        json={
            "username": "testuser",
            "email": "test1@example.com",
            "password": "password"
        }
    )
    # Attempt duplicate username
    response = client.post(
        "/register",
        json={
            "username": "testuser",
            "email": "test2@example.com",
            "password": "password"
        }
    )
    assert response.status_code == status.HTTP_409_CONFLICT
    assert "Username already taken" in response.json()["detail"]

def test_login_success(client):
    # Register user
    client.post(
        "/register",
        json={
            "username": "loginuser",
            "email": "login@example.com",
            "password": "password123"
        }
    )
    # Login
    response = client.post(
        "/login",
        json={
            "username": "loginuser",
            "password": "password123"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials(client):
    response = client.post(
        "/login",
        json={
            "username": "nonexistent",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_get_me_success(client):
    # Register and login
    client.post(
        "/register",
        json={
            "username": "meuser",
            "email": "me@example.com",
            "password": "password"
        }
    )
    login_response = client.post(
        "/login",
        json={
            "username": "meuser",
            "password": "password"
        }
    )
    token = login_response.json()["access_token"]
    
    # Get /me
    response = client.get(
        "/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["username"] == "meuser"
    assert data["email"] == "me@example.com"

def test_get_me_unauthorized(client):
    response = client.get("/me")
    assert response.status_code == status.HTTP_403_FORBIDDEN
