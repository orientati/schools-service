from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Gestione URL database per aiosqlite e asyncpg
database_url = str(settings.DATABASE_URL).strip()
if "sqlite" in database_url and "aiosqlite" not in database_url:
    database_url = database_url.replace("sqlite://", "sqlite+aiosqlite://")
    
database_url = database_url.replace("postgresql://", "postgresql+asyncpg://")
database_url = database_url.replace("postgres://", "postgresql+asyncpg://")
database_url = database_url.replace("postgresql+psycopg2://", "postgresql+asyncpg://")

# Engine e Session asincroni
engine = create_async_engine(
    database_url,
    future=True,
    echo=False,
    connect_args={"check_same_thread": False} if "sqlite" in database_url else {}
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()
