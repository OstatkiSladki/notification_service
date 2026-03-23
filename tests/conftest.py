from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from core.database import Base, get_db
from main import app
from models.notifications import Notification

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
).execution_options(schema_translate_map={"notification": None})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function", autouse=True)
def wipe_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


@pytest.fixture(scope="module")
def client() -> TestClient:
    with TestClient(app) as c:
        yield c


@pytest.fixture
def user_headers() -> dict[str, str]:
    return {"X-User-Id": "1"}


@pytest.fixture
def another_user_headers() -> dict[str, str]:
    return {"X-User-Id": "2"}


@pytest.fixture
def seed_notification() -> int:
    db = TestingSessionLocal()
    try:
        item = Notification(
            user_id=1,
            type="order_created",
            title="Заказ принят",
            message="Ваш заказ #101 принят",
            data_json={"order_id": 101},
            is_read=False,
            created_at=datetime.now(timezone.utc),
        )
        db.add(item)
        db.commit()
        db.refresh(item)
        return item.id
    finally:
        db.close()