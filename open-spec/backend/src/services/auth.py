import datetime
from fastapi import HTTPException, Request, Response, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.core.config import settings
from backend.src.core import security
from backend.src.models.user import User
from backend.src.models.refresh_token import RefreshToken
from backend.src.models.password_reset_token import PasswordResetToken
from backend.src.repositories.user import UserRepository
from backend.src.repositories.refresh_token import RefreshTokenRepository
from backend.src.repositories.password_reset_token import PasswordResetTokenRepository
from backend.src.schemas.auth import RegisterRequest, LoginRequest, ResetPasswordRequest
from backend.src.services.email import EmailService

class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)
        self.refresh_token_repo = RefreshTokenRepository(db)
        self.reset_token_repo = PasswordResetTokenRepository(db)

    async def register_user(self, data: RegisterRequest) -> User:
        # Check email uniqueness
        existing_user = await self.user_repo.get_by_email(data.email)
        if existing_user:
            raise HTTPException(status_code=409, detail="Email already registered")
        
        hashed = security.hash_password(data.password)
        new_user = User(
            email=data.email,
            full_name=data.full_name,
            hashed_password=hashed,
            role="passenger",
            is_active=True
        )
        return await self.user_repo.create(new_user)

    async def login(self, data: LoginRequest, response: Response) -> dict:
        user = await self.user_repo.get_by_email(data.email)
        if not user or not security.verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        if not user.is_active:
            raise HTTPException(status_code=403, detail="Account is disabled")

        # Create access token
        access_token = security.create_access_token(
            data={"sub": str(user.id), "email": user.email, "role": user.role}
        )

        # Create refresh token
        raw_refresh = security.generate_refresh_token()
        hashed_refresh = security.hash_token(raw_refresh)
        expires_at = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

        new_refresh = RefreshToken(
            user_id=user.id,
            token_hash=hashed_refresh,
            expires_at=expires_at
        )
        await self.refresh_token_repo.create(new_refresh)

        # Set HttpOnly cookie
        response.set_cookie(
            key="refresh_token",
            value=raw_refresh,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user
        }

    async def refresh_tokens(self, request: Request, response: Response) -> dict:
        raw_refresh = request.cookies.get("refresh_token")
        if not raw_refresh:
            raise HTTPException(status_code=401, detail="Refresh token missing")

        hashed_refresh = security.hash_token(raw_refresh)
        token_record = await self.refresh_token_repo.get_by_hash(hashed_refresh)

        if not token_record:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        # If it was already revoked, this is token reuse!
        if token_record.revoked_at is not None:
            await self.refresh_token_repo.revoke_all_for_user(token_record.user_id)
            response.delete_cookie("refresh_token")
            raise HTTPException(
                status_code=401, detail="Refresh token reuse detected — all sessions revoked"
            )

        # Check expiry
        now = datetime.datetime.now(datetime.timezone.utc)
        if token_record.expires_at < now:
            await self.refresh_token_repo.revoke(token_record)
            response.delete_cookie("refresh_token")
            raise HTTPException(status_code=401, detail="Refresh token expired")

        # Load user
        user = await self.user_repo.get_by_id(token_record.user_id)
        if not user or not user.is_active:
            response.delete_cookie("refresh_token")
            raise HTTPException(status_code=401, detail="User is inactive or not found")

        # Rotate: revoke old, create new
        await self.refresh_token_repo.revoke(token_record)

        new_raw_refresh = security.generate_refresh_token()
        new_hashed_refresh = security.hash_token(new_raw_refresh)
        new_expires_at = now + datetime.timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

        new_refresh = RefreshToken(
            user_id=user.id,
            token_hash=new_hashed_refresh,
            expires_at=new_expires_at
        )
        await self.refresh_token_repo.create(new_refresh)

        # Set new cookie
        response.set_cookie(
            key="refresh_token",
            value=new_raw_refresh,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600
        )

        # Generate new access token
        access_token = security.create_access_token(
            data={"sub": str(user.id), "email": user.email, "role": user.role}
        )

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

    async def logout(self, request: Request, response: Response) -> dict:
        raw_refresh = request.cookies.get("refresh_token")
        response.delete_cookie("refresh_token")

        if raw_refresh:
            hashed_refresh = security.hash_token(raw_refresh)
            token_record = await self.refresh_token_repo.get_by_hash(hashed_refresh)
            if token_record and token_record.revoked_at is None:
                await self.refresh_token_repo.revoke(token_record)

        return {"message": "Logged out successfully"}

    async def request_password_reset(self, email: str, background_tasks: BackgroundTasks) -> None:
        user = await self.user_repo.get_by_email(email)
        if not user:
            return

        # Invalidate previous tokens
        await self.reset_token_repo.invalidate_previous(user.id)

        # Generate token
        raw_token = security.generate_refresh_token()
        hashed_token = security.hash_token(raw_token)
        expires_at = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)

        reset_record = PasswordResetToken(
            user_id=user.id,
            token_hash=hashed_token,
            expires_at=expires_at
        )
        await self.reset_token_repo.create(reset_record)

        # Send email
        reset_url = f"http://localhost:5173/reset-password?token={raw_token}"
        EmailService.send_password_reset(background_tasks, email, reset_url)

    async def confirm_password_reset(self, data: ResetPasswordRequest) -> None:
        hashed_token = security.hash_token(data.token)
        token_record = await self.reset_token_repo.get_valid_by_hash(hashed_token)

        if not token_record:
            raise HTTPException(status_code=400, detail="Reset token expired or invalid")

        # Load user
        user = await self.user_repo.get_by_id(token_record.user_id)
        if not user or not user.is_active:
            raise HTTPException(status_code=400, detail="Reset token expired or invalid")

        # Mark token as used
        await self.reset_token_repo.mark_used(token_record)

        # Update password
        hashed_password = security.hash_password(data.new_password)
        await self.user_repo.update_password(user, hashed_password)

        # Revoke all sessions (force re-login)
        await self.refresh_token_repo.revoke_all_for_user(user.id)
