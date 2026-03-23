"""Notification business logic."""

from sqlalchemy.orm import Session

from repositories.notifications import NotificationRepository
from schemas.notifications import UpdateNotificationRequest


class NotificationService:
    """Business operations for notification entities."""

    def __init__(self) -> None:
        self.repository = NotificationRepository()

    def get_notifications(
        self,
        db: Session,
        user_id: int,
        is_read: bool | None = None,
        page: int = 1,
        limit: int = 20,
    ) -> dict:
        skip = (page - 1) * limit
        items, total = self.repository.get_by_user(
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

    def get_notification(self, db: Session, notification_id: int):
        return self.repository.get_by_id(db=db, notification_id=notification_id)

    def create_notification(
        self,
        db: Session,
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
        return self.repository.create(db=db, payload=payload)

    def update_notification(
        self,
        db: Session,
        notification_id: int,
        payload: UpdateNotificationRequest,
    ):
        notification = self.get_notification(db=db, notification_id=notification_id)
        if notification is None:
            return None

        update_data = payload.model_dump(exclude_unset=True)
        if not update_data:
            return notification

        return self.repository.update(db=db, notification=notification, payload=update_data)

    def delete_notification(self, db: Session, notification_id: int) -> bool:
        notification = self.get_notification(db=db, notification_id=notification_id)
        if notification is None:
            return False

        self.repository.delete(db=db, notification=notification)
        return True

    def mark_notification_read(self, db: Session, notification_id: int):
        notification = self.get_notification(db=db, notification_id=notification_id)
        if notification is None:
            return None

        return self.repository.mark_as_read(db=db, notification=notification)

    def mark_all_notifications_read(self, db: Session, user_id: int) -> dict:
        marked_count = self.repository.mark_all_as_read(db=db, user_id=user_id)
        return {"marked_count": marked_count}


notification_service = NotificationService()
