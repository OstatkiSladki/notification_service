import uvicorn
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from api import api_router
from core.config import get_settings


settings = get_settings()


def create_app() -> FastAPI:
    """Create and configure the FastAPI application instance."""
    app = FastAPI(
        title=settings.app_name,
        description=settings.app_description,
        version=settings.app_version,
        root_path=settings.app_root_path,
    )

    app.include_router(api_router)

    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=settings.app_debug,
    )
