import pytest
from httpx import AsyncClient, ASGITransport
from backend.src.main import app

@pytest.mark.asyncio
async def test_register_login_flow_endpoint(db_engine):
    # Use https://test as the base URL to allow secure cookies to be transmitted in tests
    async with AsyncClient(transport=ASGITransport(app=app), base_url="https://test") as client:
        # 1. Register
        register_payload = {
            "email": "endpoint_test@example.com",
            "password": "Password123",
            "full_name": "Endpoint Tester"
        }
        res = await client.post("/api/v1/auth/register", json=register_payload)
        assert res.status_code == 201
        data = res.json()
        assert data["email"] == "endpoint_test@example.com"
        assert "password" not in data

        # 2. Login
        login_payload = {
            "email": "endpoint_test@example.com",
            "password": "Password123"
        }
        res_login = await client.post("/api/v1/auth/login", json=login_payload)
        assert res_login.status_code == 200
        login_data = res_login.json()
        assert "access_token" in login_data
        assert login_data["user"]["email"] == "endpoint_test@example.com"
        assert "refresh_token" in res_login.cookies

        # 3. Refresh
        # The client automatically sends cookie back in the next request because it is HTTPS
        res_refresh = await client.post("/api/v1/auth/refresh")
        assert res_refresh.status_code == 200
        refresh_data = res_refresh.json()
        assert "access_token" in refresh_data
        assert "refresh_token" in res_refresh.cookies

        # 4. Logout
        res_logout = await client.post("/api/v1/auth/logout")
        assert res_logout.status_code == 200
        assert res_logout.json()["message"] == "Logged out successfully"
        assert res_logout.cookies.get("refresh_token") is None or res_logout.cookies.get("refresh_token") == ""
