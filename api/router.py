<<<<<<< HEAD
"""Root API router composition."""

from fastapi import APIRouter

from api.notifications import router as notifications_router

api_router = APIRouter()
api_router.include_router(notifications_router)
=======
"""Root API router composition."""

from fastapi import APIRouter

from api.notifications import router as notifications_router

api_router = APIRouter()
api_router.include_router(notifications_router)
>>>>>>> 61823b5f29fbd26f1ee9033a50b581cc288c6e36
