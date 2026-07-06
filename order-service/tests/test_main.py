from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_swagger():
    response = client.get("/docs")
    assert response.status_code == 200


def test_login_wrong_password():
    response = client.post(
        "/login",
        json={
            "username": "admin",
            "password": "wrongpassword"
        }
    )

    assert response.status_code == 401


def test_login_success():
    response = client.post(
        "/login",
        json={
            "username": "admin",
            "password": "admin123"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()