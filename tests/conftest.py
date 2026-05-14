from datetime import UTC, datetime

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from dependency import get_db_session
from main import app
from models.notifications import Notification

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def override_get_db_session():
    async with TestingSessionLocal() as db:
        yield db


app.dependency_overrides[get_db_session] = override_get_db_session


@pytest.fixture(scope="function", autouse=True)
async def wipe_database():
    async with engine.begin() as connection:
        from core.database import Base

        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)
    yield


@pytest.fixture(scope="module")
async def client() -> AsyncClient:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c


@pytest.fixture
def user_headers() -> dict[str, str]:
    return {"X-User-ID": "1"}


@pytest.fixture
def another_user_headers() -> dict[str, str]:
    return {"X-User-ID": "2"}


@pytest.fixture
async def seed_notification() -> int:
    async with TestingSessionLocal() as db:
        item = Notification(
            user_id=1,
            type="order_created",
            title="Заказ принят",
            message="Ваш заказ #101 принят",
            data_json={"order_id": 101},
            is_read=False,
            created_at=datetime.now(UTC),
        )
        db.add(item)
        await db.commit()
        await db.refresh(item)
        return item.id
