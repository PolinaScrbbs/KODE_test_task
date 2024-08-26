import requests

BASE_URL = "http://localhost:8080"  # URL вашего запущенного FastAPI приложения


def test_register_user():
    response = requests.post(
        f"{BASE_URL}/auth/register",
        json={"email": "newuser@example.com", "password": "newpassword"},
    )
    assert response.status_code == 201


def test_register_existing_user():
    requests.post(
        f"{BASE_URL}/auth/register",
        json={"email": "existinguser@example.com", "password": "somepassword"},
    )

    response = requests.post(
        f"{BASE_URL}/auth/register",
        json={"email": "existinguser@example.com", "password": "somepassword"},
    )
    assert response.status_code == 400


def test_login_user():
    requests.post(
        f"{BASE_URL}/auth/register",
        json={"email": "testuser@example.com", "password": "testpassword"},
    )

    response = requests.post(
        f"{BASE_URL}/auth/jwt/login",
        data={"username": "testuser@example.com", "password": "testpassword"},
    )
    assert response.status_code == 204
