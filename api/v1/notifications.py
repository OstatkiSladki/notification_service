from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependency import CurrentUser, get_current_user, get_db_session
from schemas.notifications import (
    NotificationFilterParams,
    NotificationListResponse,
    NotificationResponse,
    UpdateNotificationRequest,
)
from services.notifications import notification_service

router = APIRouter(prefix="/notifications", tags=["Notifications"])


async def get_valid_notification(
    notification_id: int = Path(..., description="ID уведомления"),
    current_user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
):
    notification = await notification_service.get_notification(
        db=db, notification_id=notification_id
    )
    if notification is None or notification.user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
    return notification


@router.get(
    "",
    response_model=NotificationListResponse,
    status_code=status.HTTP_200_OK,
    response_description="Список уведомлений",
    summary="Получить список уведомлений пользователя",
    description="Возвращает уведомления текущего пользователя",
)
async def get_notifications(
    filters: Annotated[NotificationFilterParams, Query()],
    current_user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> NotificationListResponse:
    """Get notifications for the current user."""
    result = await notification_service.get_notifications(
        db=db,
        user_id=current_user.user_id,
        is_read=filters.is_read,
        page=filters.page,
        limit=filters.limit,
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
async def get_notification(
    notification=Depends(get_valid_notification),
) -> NotificationResponse:
    """Get a single notification by its identifier."""
    return NotificationResponse.model_validate(notification)


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
    existing=Depends(get_valid_notification),
    db: AsyncSession = Depends(get_db_session),
) -> NotificationResponse:
    """Update notification content by identifier."""
    notification = await notification_service.update_notification(
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
async def delete_notification(
    notification_id: int = Path(..., description="ID уведомления"),
    existing=Depends(get_valid_notification),
    db: AsyncSession = Depends(get_db_session),
) -> None:
    """Delete a notification by identifier."""
    await notification_service.delete_notification(db=db, notification_id=notification_id)


@router.patch(
    "/{notification_id}/read",
    status_code=status.HTTP_200_OK,
    response_description="Уведомление отмечено как прочитанное",
    summary="Отметить уведомление как прочитанное",
)
async def mark_notification_read(
    notification_id: int = Path(..., description="ID уведомления"),
    existing=Depends(get_valid_notification),
    db: AsyncSession = Depends(get_db_session),
) -> Response:
    """Mark a single notification as read."""
    await notification_service.mark_notification_read(db=db, notification_id=notification_id)
    return Response(status_code=status.HTTP_200_OK)


@router.post(
    "/mark-all-read",
    status_code=status.HTTP_200_OK,
    response_description="Все уведомления отмечены как прочитанные",
    summary="Отметить все уведомления как прочитанные",
)
async def mark_all_notifications_read(
    current_user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> Response:
    """Mark all notifications for the current user as read."""
    await notification_service.mark_all_notifications_read(db=db, user_id=current_user.user_id)
    return Response(status_code=status.HTTP_200_OK)
