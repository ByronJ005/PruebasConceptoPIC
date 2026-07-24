import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from backend.src.models.refresh_token import RefreshToken

class RefreshTokenRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, refresh_token: RefreshToken) -> RefreshToken:
        self.db.add(refresh_token)
        await self.db.commit()
        await self.db.refresh(refresh_token)
        return refresh_token

    async def get_by_hash(self, token_hash: str) -> RefreshToken | None:
        result = await self.db.execute(select(RefreshToken).where(RefreshToken.token_hash == token_hash))
        return result.scalars().first()

    async def revoke(self, refresh_token: RefreshToken) -> RefreshToken:
        refresh_token.revoked_at = datetime.datetime.now(datetime.timezone.utc)
        self.db.add(refresh_token)
        await self.db.commit()
        await self.db.refresh(refresh_token)
        return refresh_token

    async def revoke_all_for_user(self, user_id: int) -> None:
        now = datetime.datetime.now(datetime.timezone.utc)
        await self.db.execute(
            update(RefreshToken)
            .where(RefreshToken.user_id == user_id, RefreshToken.revoked_at == None)
            .values(revoked_at=now)
        )
        await self.db.commit()
