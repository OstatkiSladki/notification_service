"""Notification API routes."""

from fastapi import APIRouter, Path, Query, status

from schemas.notifications import (
    NotificationListResponse,
    NotificationResponse,
    UpdateNotificationRequest,
)

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get(
    "",
    response_model=NotificationListResponse,
    status_code=status.HTTP_200_OK,
    response_description="Список уведомлений",
    summary="Получить список уведомлений пользователя",
    description="Возвращает уведомления текущего пользователя",
)
async def get_notifications(
    is_read: bool | None = Query(
        default=None,
        description="Фильтр по статусу прочтения",
    ),
    page: int = Query(default=1),
    limit: int = Query(default=20, le=100),
) -> NotificationListResponse:
    """Get notifications for the current user."""
    raise NotImplementedError("Business logic for listing notifications is not implemented yet.")


@router.get(
    "/{notification_id}",
    response_model=NotificationResponse,
    status_code=status.HTTP_200_OK,
    response_description="Уведомление найдено",
    summary="Получить конкретное уведомление",
    responses={404: {"description": "Уведомление не найдено"}},
)
async def get_notification(
    notification_id: int = Path(..., description="ID уведомления"),
) -> NotificationResponse:
    """Get a single notification by its identifier."""
    raise NotImplementedError("Business logic for getting one notification is not implemented yet.")


@router.patch(
    "/{notification_id}",
    response_model=NotificationResponse,
    status_code=status.HTTP_200_OK,
    response_description="Уведомление обновлено",
    summary="Обновить уведомление",
    description="Используется для изменения текста или данных уведомления",
)
async def update_notification(
    payload: UpdateNotificationRequest,
    notification_id: int = Path(..., description="ID уведомления"),
) -> NotificationResponse:
    """Update notification content by identifier."""
    raise NotImplementedError("Business logic for updating a notification is not implemented yet.")


@router.delete(
    "/{notification_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="Уведомление удалено",
    summary="Удалить уведомление",
)
async def delete_notification(
    notification_id: int = Path(..., description="ID уведомления"),
) -> None:
    """Delete a notification by identifier."""
    raise NotImplementedError("Business logic for deleting a notification is not implemented yet.")


@router.patch(
    "/{notification_id}/read",
    status_code=status.HTTP_200_OK,
    response_description="Уведомление отмечено как прочитанное",
    summary="Отметить уведомление как прочитанное",
)
async def mark_notification_read(
    notification_id: int = Path(..., description="ID уведомления"),
) -> None:
    """Mark a single notification as read."""
    raise NotImplementedError("Business logic for marking a notification as read is not implemented yet.")


@router.post(
    "/mark-all-read",
    status_code=status.HTTP_200_OK,
    response_description="Все уведомления отмечены как прочитанные",
    summary="Отметить все уведомления как прочитанные",
)
async def mark_all_notifications_read() -> None:
    """Mark all notifications for the current user as read."""
    raise NotImplementedError("Business logic for marking all notifications as read is not implemented yet.")
