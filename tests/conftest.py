import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.api.deps import get_db
import os
os.environ["SCHOOLS_ENVIRONMENT"] = "testing"
from app.main import app
from app.core.config import settings
settings.ENVIRONMENT = "testing"
from unittest.mock import patch, AsyncMock

# DB in memoria per i test (aiosqlite)
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(
    bind=engine, 
    class_=AsyncSession,
    autocommit=False, 
    autoflush=False
)

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest.fixture(scope="session", autouse=True)
def mock_broker():
    with patch("app.services.broker.AsyncBrokerSingleton") as MockBroker:
        instance = MockBroker.return_value
        instance.connect = AsyncMock(return_value=True)
        instance.subscribe = AsyncMock()
        instance.close = AsyncMock()
        yield instance

@pytest.fixture(scope="function")
async def db_session():
    # Setup DB
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Create session
    async with TestingSessionLocal() as session:
        # Override get_db
        async def override_get_db():
            yield session
        
        app.dependency_overrides[get_db] = override_get_db
        yield session
    
    # Teardown
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope="function")
async def client(db_session):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
