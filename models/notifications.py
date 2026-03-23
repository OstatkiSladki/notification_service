"""SQLAlchemy ORM model for notifications."""

from datetime import datetime, timezone

from sqlalchemy import JSON, BigInteger, Boolean, Column, DateTime, Integer, String, Text

from core.config import get_settings
from core.database import Base


def utc_now() -> datetime:
    """Return timezone-aware UTC datetime."""
    return datetime.now(timezone.utc)


class Notification(Base):
    """Notification entity stored in database."""

    __tablename__ = "notifications"
    _settings = get_settings()
    if not _settings.database_url.startswith("sqlite"):
        __table_args__ = {"schema": "notification"}

    id = Column(
        BigInteger().with_variant(Integer, "sqlite"),
        primary_key=True,
        autoincrement=True,
        index=True,
    )
    user_id = Column(BigInteger().with_variant(Integer, "sqlite"), nullable=False, index=True)
    type = Column(String(50), nullable=False, index=True)
    title = Column(String(255), nullable=True)
    message = Column(Text, nullable=False)
    data_json = Column(JSON, default=dict, nullable=True)
    is_read = Column(Boolean, default=False, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    read_at = Column(DateTime(timezone=True), nullable=True)
