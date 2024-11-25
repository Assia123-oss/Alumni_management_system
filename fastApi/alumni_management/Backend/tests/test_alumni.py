import pytest
from fastapi.testclient import TestClient

def test_create_alumni(client):
    # First create a user
    user_response = client.post(
        "/users/",
        json={
            "email": "alumni@example.com",
            "password": "testpassword",
            "first_name": "Test",
            "last_name": "Alumni",
            "is_admin": False
        }
    )
    assert user_response.status_code == 200

    # Login to get token
    login_response = client.post(
        "/users/token",  # Updated path
        data={
            "username": "alumni@example.com",
            "password": "testpassword"
        }
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    # Then create an alumni profile with authentication
    response = client.post(
        "/alumni/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "graduation_year": 2020,
            "degree": "Bachelor of Science",
            "major": "Computer Science",
            "current_job": "Software Engineer"
        }
    )
    assert response.status_code == 200