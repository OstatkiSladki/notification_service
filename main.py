"""Application entrypoint for Notification Service."""

import uvicorn
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from api.router import api_router
from core.config import get_settings

settings = get_settings()


def create_app() -> FastAPI:
    """Create and configure the FastAPI application instance."""
    app = FastAPI(
        title=settings.app_name,
        description=settings.app_description,
        version=settings.app_version,
        servers=[
            {
                "url": "https://api.company.com/notifications",
                "description": "Production",
            },
            {
                "url": "http://localhost:8003",
                "description": "Local development",
            },
        ],
        openapi_tags=[
            {
                "name": "Notifications",
                "description": "Операции с уведомлениями пользователя",
            }
        ],
    )

    app.include_router(api_router, prefix=settings.api_v1_prefix)

    def custom_openapi() -> dict:
        """Add CookieAuth to generated OpenAPI schema."""
        if app.openapi_schema is not None:
            return app.openapi_schema

        openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
            tags=app.openapi_tags,
        )

        components = openapi_schema.setdefault("components", {})
        security_schemes = components.setdefault("securitySchemes", {})
        security_schemes["CookieAuth"] = {
            "type": "apiKey",
            "in": "cookie",
            "name": "access_token",
        }
        openapi_schema["security"] = [{"CookieAuth": []}]

        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi
    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
    )
