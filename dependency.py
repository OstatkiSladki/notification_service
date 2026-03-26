from collections.abc import AsyncIterator

from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db_session as core_get_db_session
from core.security import require_user_id


class CurrentUser(BaseModel):
    user_id: int


async def get_db_session() -> AsyncIterator[AsyncSession]:
    async for session in core_get_db_session():
        yield session


def get_current_user(user_id: int = Depends(require_user_id)) -> CurrentUser:
    return CurrentUser(user_id=user_id)
