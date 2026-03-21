"""Root API router composition."""

from fastapi import APIRouter

from api.notifications import router as notifications_router

api_router = APIRouter()
api_router.include_router(notifications_router)
