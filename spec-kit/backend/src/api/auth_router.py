from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.core.config import settings
from src.core.security import create_access_token, create_refresh_token
from src.schemas.user_schema import (
    UserCreate,
    UserLogin,
    UserResponse,
    Token,
    PasswordRecoveryRequest,
    PasswordReset
)
from src.services import auth_service

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    db_user = auth_service.get_user_by_email(db, email=user_in.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
    user = auth_service.create_user(db, email=user_in.email, password=user_in.password)
    return user

@router.post("/login", response_model=Token)
def login(
    user_in: UserLogin,
    response: Response,
    db: Session = Depends(get_db)
):
    user = auth_service.authenticate_user(db, email=user_in.email, password=user_in.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    access_token = create_access_token(subject=user.id)
    refresh_token = create_refresh_token(subject=user.id)
    
    # Set HTTP-Only Cookie for Refresh Token
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        max_age=7 * 24 * 60 * 60,  # 7 days
        secure=False,  # Set to True in production
        samesite="lax"
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(
        key="refresh_token",
        httponly=True,
        secure=False,
        samesite="lax"
    )
    return {"message": "Successfully logged out"}

@router.post("/password-recovery")
def request_recovery(recovery_in: PasswordRecoveryRequest, db: Session = Depends(get_db)):
    # To prevent email enumeration, we return 200 even if the user is not found,
    # but the service only generates a token if the user exists.
    token = auth_service.generate_recovery_token(db, email=recovery_in.email)
    
    # In a real app, send the email here. We will log it.
    if token:
        print(f"Password reset link generated: http://localhost:5173/password-reset?token={token}")
        
    return {"message": "If the email is registered, a password recovery link has been sent"}

@router.post("/password-reset")
def reset_password(reset_in: PasswordReset, db: Session = Depends(get_db)):
    success = auth_service.verify_and_use_recovery_token(
        db, token=reset_in.token, new_password=reset_in.new_password
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired token"
        )
    return {"message": "Password reset successfully"}
