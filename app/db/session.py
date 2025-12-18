from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

<<<<<<< HEAD
# Gestione URL database per aiosqlite
database_url = settings.DATABASE_URL
if database_url.startswith("sqlite://") and "aiosqlite" not in database_url:
    database_url = database_url.replace("sqlite://", "sqlite+aiosqlite://")
=======
# Gestione URL database per aiosqlite e asyncpg
database_url = str(settings.DATABASE_URL).strip()
if "sqlite" in database_url and "aiosqlite" not in database_url:
    database_url = database_url.replace("sqlite://", "sqlite+aiosqlite://")
    
database_url = database_url.replace("postgresql://", "postgresql+asyncpg://")
database_url = database_url.replace("postgres://", "postgresql+asyncpg://")
database_url = database_url.replace("postgresql+psycopg2://", "postgresql+asyncpg://")
>>>>>>> 1804c8e (Refactor: Async services/routes restoration and RabbitMQ fix)

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
