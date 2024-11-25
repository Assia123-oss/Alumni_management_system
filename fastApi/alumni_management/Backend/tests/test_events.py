import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta

def test_create_event(client):
    # First create a user with admin privileges
    user_response = client.post(
        "/users/",
        json={
            "email": "admin@example.com",
            "password": "adminpass",
            "first_name": "Admin",
            "last_name": "User",
            "is_admin": True
        }
    )
    assert user_response.status_code == 200

    # Login to get token
    login_response = client.post(
        "/users/token",  # Updated path
        data={
            "username": "admin@example.com",
            "password": "adminpass"
        }
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    # Create event with authentication
    future_date = (datetime.now() + timedelta(days=7)).isoformat()
    response = client.post(
        "/events/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Test Event",
            "description": "Test Description",
            "date": future_date,
            "location": "Test Location",
            "max_participants": 100
        }
    )
    assert response.status_code == 200