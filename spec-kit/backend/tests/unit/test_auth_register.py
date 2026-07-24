from fastapi.testclient import TestClient

def test_register_user_success(client: TestClient):
    response = client.post(
        "/api/auth/register",
        json={"email": "newuser@example.com", "password": "SecurePassword123!"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert "id" in data

def test_register_user_duplicate_email(client: TestClient):
    # Register once
    response = client.post(
        "/api/auth/register",
        json={"email": "dup@example.com", "password": "SecurePassword123!"}
    )
    assert response.status_code == 201
    
    # Register second time
    response = client.post(
        "/api/auth/register",
        json={"email": "dup@example.com", "password": "SecurePassword123!"}
    )
    assert response.status_code == 409
    assert response.json()["detail"] == "Email already registered"

def test_register_user_weak_password(client: TestClient):
    response = client.post(
        "/api/auth/register",
        json={"email": "weak@example.com", "password": "123"}
    )
    assert response.status_code == 422
    
    # Check custom formatting from exception handler
    data = response.json()
    assert "errors" in data
    # Password complexity fails
    response = client.post(
        "/api/auth/register",
        json={"email": "weak2@example.com", "password": "justletters"}
    )
    assert response.status_code == 422
