"""Notification API routes."""

from fastapi import APIRouter, Depends, HTTPException, Path, Query, Response, status
from sqlalchemy.orm import Session

from core.database import get_db
from core.security import get_current_user_id
from services.notifications import notification_service

from schemas.notifications import NotificationListResponse, NotificationResponse, UpdateNotificationRequest

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get(
    "",
    response_model=NotificationListResponse,
    status_code=status.HTTP_200_OK,
    response_description="Список уведомлений",
    summary="Получить список уведомлений пользователя",
    description="Возвращает уведомления текущего пользователя",
)
def get_notifications(
    is_read: bool | None = Query(
        default=None,
        description="Фильтр по статусу прочтения",
    ),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, le=100),
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> NotificationListResponse:
    """Get notifications for the current user."""
    result = notification_service.get_notifications(
        db=db,
        user_id=user_id,
        is_read=is_read,
        page=page,
        limit=limit,
    )
    return NotificationListResponse.model_validate(result)


@router.get(
    "/{notification_id}",
    response_model=NotificationResponse,
    status_code=status.HTTP_200_OK,
    response_description="Уведомление найдено",
    summary="Получить конкретное уведомление",
    responses={404: {"description": "Уведомление не найдено"}},
)
def get_notification(
    notification_id: int = Path(..., description="ID уведомления"),
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> NotificationResponse:
    """Get a single notification by its identifier."""
    notification = notification_service.get_notification(db=db, notification_id=notification_id)
    if notification is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
    if notification.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
    return NotificationResponse.model_validate(notification)


@router.patch(
    "/{notification_id}",
    response_model=NotificationResponse,
    status_code=status.HTTP_200_OK,
    response_description="Уведомление обновлено",
    summary="Обновить уведомление",
    description="Используется для изменения текста или данных уведомления",
)
def update_notification(
    payload: UpdateNotificationRequest,
    notification_id: int = Path(..., description="ID уведомления"),
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> NotificationResponse:
    """Update notification content by identifier."""
    existing = notification_service.get_notification(db=db, notification_id=notification_id)
    if existing is None or existing.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")

    notification = notification_service.update_notification(
        db=db,
        notification_id=notification_id,
        payload=payload,
    )
    if notification is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
    return NotificationResponse.model_validate(notification)


@router.delete(
    "/{notification_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="Уведомление удалено",
    summary="Удалить уведомление",
)
def delete_notification(
    notification_id: int = Path(..., description="ID уведомления"),
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> None:
    """Delete a notification by identifier."""
    notification = notification_service.get_notification(db=db, notification_id=notification_id)
    if notification is None or notification.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")

    notification_service.delete_notification(db=db, notification_id=notification_id)


@router.patch(
    "/{notification_id}/read",
    status_code=status.HTTP_200_OK,
    response_description="Уведомление отмечено как прочитанное",
    summary="Отметить уведомление как прочитанное",
)
def mark_notification_read(
    notification_id: int = Path(..., description="ID уведомления"),
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> Response:
    """Mark a single notification as read."""
    notification = notification_service.get_notification(db=db, notification_id=notification_id)
    if notification is None or notification.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")

    notification_service.mark_notification_read(db=db, notification_id=notification_id)
    return Response(status_code=status.HTTP_200_OK)


@router.post(
    "/mark-all-read",
    status_code=status.HTTP_200_OK,
    response_description="Все уведомления отмечены как прочитанные",
    summary="Отметить все уведомления как прочитанные",
)
def mark_all_notifications_read(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> Response:
    """Mark all notifications for the current user as read."""
    notification_service.mark_all_notifications_read(db=db, user_id=user_id)
    return Response(status_code=status.HTTP_200_OK)
