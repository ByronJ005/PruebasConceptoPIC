import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from backend.src.models.password_reset_token import PasswordResetToken

class PasswordResetTokenRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, reset_token: PasswordResetToken) -> PasswordResetToken:
        self.db.add(reset_token)
        await self.db.commit()
        await self.db.refresh(reset_token)
        return reset_token

    async def get_valid_by_hash(self, token_hash: str) -> PasswordResetToken | None:
        now = datetime.datetime.now(datetime.timezone.utc)
        result = await self.db.execute(
            select(PasswordResetToken).where(
                PasswordResetToken.token_hash == token_hash,
                PasswordResetToken.used_at == None,
                PasswordResetToken.expires_at > now
            )
        )
        return result.scalars().first()

    async def invalidate_previous(self, user_id: int) -> None:
        now = datetime.datetime.now(datetime.timezone.utc)
        await self.db.execute(
            update(PasswordResetToken)
            .where(PasswordResetToken.user_id == user_id, PasswordResetToken.used_at == None)
            .values(used_at=now)
        )
        await self.db.commit()

    async def mark_used(self, reset_token: PasswordResetToken) -> PasswordResetToken:
        reset_token.used_at = datetime.datetime.now(datetime.timezone.utc)
        self.db.add(reset_token)
        await self.db.commit()
        await self.db.refresh(reset_token)
        return reset_token
