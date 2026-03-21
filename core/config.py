"""Application configuration loaded from environment variables."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings for the Notification Service."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    app_name: str = Field(default="Notification Service API")
    app_description: str = Field(
        default=(
            "Сервис управления уведомлениями пользователей.\n\n"
            "## Источник уведомлений\n"
            "Уведомления создаются асинхронно через RabbitMQ события от других сервисов:\n"
            "- Order Service\n"
            "- Offer Service\n"
            "- Auth Service\n\n"
            "## Основные функции API\n"
            "- Получение списка уведомлений\n"
            "- Просмотр конкретного уведомления\n"
            "- Отметка уведомлений как прочитанных\n"
            "- Удаление уведомлений\n"
            "- Редактирование уведомлений (админ)"
        )
    )
    app_version: str = Field(default="1.0.0")
    api_v1_prefix: str = Field(default="/api/v1")

    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8003)
    reload: bool = Field(default=True)


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings."""
    return Settings()
