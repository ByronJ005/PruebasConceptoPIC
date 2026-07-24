import pytest
import datetime
from fastapi import HTTPException
from unittest.mock import MagicMock

from backend.src.services.auth import AuthService
from backend.src.schemas.auth import RegisterRequest, LoginRequest, ResetPasswordRequest
from backend.src.core import security
from backend.src.models.user import User
from backend.src.models.refresh_token import RefreshToken
from backend.src.models.password_reset_token import PasswordResetToken

@pytest.mark.asyncio
async def test_register_user_success(db_session):
    auth_service = AuthService(db_session)
    data = RegisterRequest(
        email="test_reg@example.com",
        password="Password123",
        full_name="Test User"
    )
    user = await auth_service.register_user(data)
    assert user.id is not None
    assert user.email == "test_reg@example.com"
    assert user.role == "passenger"
    assert security.verify_password("Password123", user.hashed_password)

@pytest.mark.asyncio
async def test_register_user_duplicate_email(db_session):
    auth_service = AuthService(db_session)
    data = RegisterRequest(
        email="dup@example.com",
        password="Password123",
        full_name="Dup User"
    )
    await auth_service.register_user(data)
    
    with pytest.raises(HTTPException) as exc_info:
        await auth_service.register_user(data)
    assert exc_info.value.status_code == 409

@pytest.mark.asyncio
async def test_login_success(db_session):
    auth_service = AuthService(db_session)
    reg_data = RegisterRequest(
        email="login_ok@example.com",
        password="Password123",
        full_name="Login Ok"
    )
    user = await auth_service.register_user(reg_data)
    
    mock_response = MagicMock()
    login_data = LoginRequest(email="login_ok@example.com", password="Password123")
    result = await auth_service.login(login_data, mock_response)
    
    assert "access_token" in result
    assert result["user"].id == user.id
    mock_response.set_cookie.assert_called_once()

@pytest.mark.asyncio
async def test_login_wrong_credentials(db_session):
    auth_service = AuthService(db_session)
    mock_response = MagicMock()
    login_data = LoginRequest(email="nonexistent@example.com", password="Password123")
    with pytest.raises(HTTPException) as exc_info:
        await auth_service.login(login_data, mock_response)
    assert exc_info.value.status_code == 401

@pytest.mark.asyncio
async def test_refresh_tokens_success(db_session):
    auth_service = AuthService(db_session)
    reg_data = RegisterRequest(
        email="refresh_ok@example.com",
        password="Password123",
        full_name="Refresh Ok"
    )
    user = await auth_service.register_user(reg_data)
    
    mock_response = MagicMock()
    login_data = LoginRequest(email="refresh_ok@example.com", password="Password123")
    await auth_service.login(login_data, mock_response)
    
    args, kwargs = mock_response.set_cookie.call_args
    raw_token = kwargs.get("value") or args[1]
    
    mock_request = MagicMock()
    mock_request.cookies = {"refresh_token": raw_token}
    
    mock_response_refresh = MagicMock()
    refresh_result = await auth_service.refresh_tokens(mock_request, mock_response_refresh)
    assert "access_token" in refresh_result
    mock_response_refresh.set_cookie.assert_called_once()

@pytest.mark.asyncio
async def test_refresh_tokens_reuse_detection(db_session):
    auth_service = AuthService(db_session)
    reg_data = RegisterRequest(
        email="reuse@example.com",
        password="Password123",
        full_name="Reuse"
    )
    user = await auth_service.register_user(reg_data)
    
    mock_response = MagicMock()
    login_data = LoginRequest(email="reuse@example.com", password="Password123")
    await auth_service.login(login_data, mock_response)
    
    args, kwargs = mock_response.set_cookie.call_args
    raw_token = kwargs.get("value") or args[1]
    
    mock_request_1 = MagicMock()
    mock_request_1.cookies = {"refresh_token": raw_token}
    mock_response_1 = MagicMock()
    await auth_service.refresh_tokens(mock_request_1, mock_response_1)
    
    mock_request_2 = MagicMock()
    mock_request_2.cookies = {"refresh_token": raw_token}
    mock_response_2 = MagicMock()
    with pytest.raises(HTTPException) as exc_info:
        await auth_service.refresh_tokens(mock_request_2, mock_response_2)
    
    assert exc_info.value.status_code == 401
    assert "reuse detected" in exc_info.value.detail

@pytest.mark.asyncio
async def test_logout_success(db_session):
    auth_service = AuthService(db_session)
    reg_data = RegisterRequest(
        email="logout@example.com",
        password="Password123",
        full_name="Logout User"
    )
    await auth_service.register_user(reg_data)
    
    mock_response = MagicMock()
    login_data = LoginRequest(email="logout@example.com", password="Password123")
    await auth_service.login(login_data, mock_response)
    
    args, kwargs = mock_response.set_cookie.call_args
    raw_token = kwargs.get("value") or args[1]
    
    mock_request = MagicMock()
    mock_request.cookies = {"refresh_token": raw_token}
    mock_response_logout = MagicMock()
    
    logout_result = await auth_service.logout(mock_request, mock_response_logout)
    assert logout_result["message"] == "Logged out successfully"
    mock_response_logout.delete_cookie.assert_called_with("refresh_token")
    
@pytest.mark.asyncio
async def test_password_recovery_success_with_mock_uuid(db_session, monkeypatch):
    fixed_uuid = "11111111-2222-3333-4444-555555555555"
    monkeypatch.setattr(security, "generate_refresh_token", lambda: fixed_uuid)
    
    auth_service = AuthService(db_session)
    reg_data = RegisterRequest(
        email="recover_mock@example.com",
        password="OldPassword123",
        full_name="Mock User"
    )
    user = await auth_service.register_user(reg_data)
    
    mock_bg_tasks = MagicMock()
    await auth_service.request_password_reset("recover_mock@example.com", mock_bg_tasks)
    
    reset_data = ResetPasswordRequest(token=fixed_uuid, new_password="NewPassword123")
    await auth_service.confirm_password_reset(reset_data)
    
    mock_response = MagicMock()
    login_data = LoginRequest(email="recover_mock@example.com", password="NewPassword123")
    login_result = await auth_service.login(login_data, mock_response)
    assert login_result["user"].id == user.id
