import asyncio
import pytest
import pytest_asyncio
from typing import AsyncGenerator
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from backend.src.core.config import settings
from backend.src.db.base_class import Base
from backend.src.main import app
from backend.src.db.session import get_db

@pytest.fixture(scope="session")
def event_loop():
    try:
        return asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop

@pytest_asyncio.fixture(scope="session")
async def db_engine():
    # Use NullPool to ensure connections are closed immediately
    engine = create_async_engine(settings.DATABASE_URL, echo=False, poolclass=pool.NullPool)
    
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    yield engine
    
    # Drop tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        
    await engine.dispose()

@pytest_asyncio.fixture
async def db_session(db_engine) -> AsyncGenerator[AsyncSession, None]:
    async_session = async_sessionmaker(
        bind=db_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    
    async with async_session() as session:
        yield session
        try:
            await session.rollback()
            await session.close()
        except Exception:
            pass

@pytest_asyncio.fixture(autouse=True)
async def override_get_db_dependency(db_session):
    async def _get_db_override():
        yield db_session
    app.dependency_overrides[get_db] = _get_db_override
    yield
    app.dependency_overrides.clear()
