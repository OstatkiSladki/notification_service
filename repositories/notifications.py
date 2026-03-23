"""Notification repository layer."""

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from models.notifications import Notification


class NotificationRepository:
    """Low-level CRUD operations for notifications."""

    def create(self, db: Session, payload: dict) -> Notification:
        notification = Notification(**payload)
        db.add(notification)
        db.commit()
        db.refresh(notification)
        return notification

    def get_by_id(self, db: Session, notification_id: int) -> Notification | None:
        return (
            db.query(Notification)
            .filter(Notification.id == notification_id)
            .first()
        )

    def get_by_user(
        self,
        db: Session,
        user_id: int,
        is_read: bool | None = None,
        skip: int = 0,
        limit: int = 20,
    ) -> tuple[list[Notification], int]:
        query = db.query(Notification).filter(Notification.user_id == user_id)
        if is_read is not None:
            query = query.filter(Notification.is_read == is_read)

        total = query.count()
        items = (
            query
            .order_by(Notification.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return items, total

    def update(self, db: Session, notification: Notification, payload: dict) -> Notification:
        for key, value in payload.items():
            setattr(notification, key, value)
        db.commit()
        db.refresh(notification)
        return notification

    def delete(self, db: Session, notification: Notification) -> None:
        db.delete(notification)
        db.commit()

    def mark_as_read(self, db: Session, notification: Notification) -> Notification:
        if notification.is_read:
            return notification

        payload = {
            "is_read": True,
            "read_at": datetime.now(timezone.utc),
        }
        return self.update(db, notification, payload)

    def mark_all_as_read(self, db: Session, user_id: int) -> int:
        marked_count = (
            db.query(Notification)
            .filter(Notification.user_id == user_id, Notification.is_read.is_(False))
            .update(
                {
                    Notification.is_read: True,
                    Notification.read_at: datetime.now(timezone.utc),
                },
                synchronize_session=False,
            )
        )
        db.commit()
        return marked_count
