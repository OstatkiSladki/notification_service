from datetime import UTC, datetime

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from models.notifications import Notification


class NotificationRepository:

    async def create(self, db: AsyncSession, payload: dict) -> Notification:
        notification = Notification(**payload)
        db.add(notification)
        await db.commit()
        await db.refresh(notification)
        return notification

    async def get_by_id(self, db: AsyncSession, notification_id: int) -> Notification | None:
        result = await db.execute(select(Notification).where(Notification.id == notification_id))
        return result.scalar_one_or_none()

    async def get_by_user(
        self,
        db: AsyncSession,
        user_id: int,
        is_read: bool | None = None,
        skip: int = 0,
        limit: int = 20,
    ) -> tuple[list[Notification], int]:
        base_query = select(Notification).where(Notification.user_id == user_id)
        if is_read is not None:
            base_query = base_query.where(Notification.is_read == is_read)

        total_result = await db.execute(select(func.count()).select_from(base_query.subquery()))
        total = int(total_result.scalar_one())

        items_result = await db.execute(
            base_query.order_by(Notification.created_at.desc()).offset(skip).limit(limit)
        )
        items = list(items_result.scalars().all())
        return items, total

    async def update(
        self, db: AsyncSession, notification: Notification, payload: dict
    ) -> Notification:
        for key, value in payload.items():
            setattr(notification, key, value)
        await db.commit()
        await db.refresh(notification)
        return notification

    async def delete(self, db: AsyncSession, notification: Notification) -> None:
        await db.delete(notification)
        await db.commit()

    async def mark_as_read(self, db: AsyncSession, notification: Notification) -> Notification:
        if notification.is_read:
            return notification

        payload = {
            "is_read": True,
            "read_at": datetime.now(UTC),
        }
        return await self.update(db, notification, payload)

    async def mark_all_as_read(self, db: AsyncSession, user_id: int) -> int:
        statement = (
            update(Notification)
            .where(Notification.user_id == user_id, Notification.is_read.is_(False))
            .values(is_read=True, read_at=datetime.now(UTC))
        )
        result = await db.execute(statement)
        await db.commit()
        return int(result.rowcount or 0)
