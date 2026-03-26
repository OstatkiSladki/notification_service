from sqlalchemy.ext.asyncio import AsyncSession

from repositories.notifications import NotificationRepository
from schemas.notifications import UpdateNotificationRequest


class NotificationService:

    def __init__(self) -> None:
        self.repository = NotificationRepository()

    async def get_notifications(
        self,
        db: AsyncSession,
        user_id: int,
        is_read: bool | None = None,
        page: int = 1,
        limit: int = 20,
    ) -> dict:
        skip = (page - 1) * limit
        items, total = await self.repository.get_by_user(
            db=db,
            user_id=user_id,
            is_read=is_read,
            skip=skip,
            limit=limit,
        )
        return {
            "items": items,
            "total": total,
            "page": page,
            "limit": limit,
        }

    async def get_notification(self, db: AsyncSession, notification_id: int):
        return await self.repository.get_by_id(db=db, notification_id=notification_id)

    async def create_notification(
        self,
        db: AsyncSession,
        user_id: int,
        notification_type: str,
        title: str,
        message: str,
        data_json: dict | None = None,
    ):
        payload = {
            "user_id": user_id,
            "type": notification_type,
            "title": title,
            "message": message,
            "data_json": data_json,
        }
        return await self.repository.create(db=db, payload=payload)

    async def update_notification(
        self,
        db: AsyncSession,
        notification_id: int,
        payload: UpdateNotificationRequest,
    ):
        notification = await self.get_notification(db=db, notification_id=notification_id)
        if notification is None:
            return None

        update_data = payload.model_dump(exclude_unset=True)
        if not update_data:
            return notification

        return await self.repository.update(db=db, notification=notification, payload=update_data)

    async def delete_notification(self, db: AsyncSession, notification_id: int) -> bool:
        notification = await self.get_notification(db=db, notification_id=notification_id)
        if notification is None:
            return False

        await self.repository.delete(db=db, notification=notification)
        return True

    async def mark_notification_read(self, db: AsyncSession, notification_id: int):
        notification = await self.get_notification(db=db, notification_id=notification_id)
        if notification is None:
            return None

        return await self.repository.mark_as_read(db=db, notification=notification)

    async def mark_all_notifications_read(self, db: AsyncSession, user_id: int) -> dict:
        marked_count = await self.repository.mark_all_as_read(db=db, user_id=user_id)
        return {"marked_count": marked_count}


notification_service = NotificationService()
