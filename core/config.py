from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

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
    app_root_path: str = Field(default="")

    app_host: str = Field(default="0.0.0.0")
    app_port: int = Field(default=8005)
    app_debug: bool = Field(default=False)
    log_level: str = Field(default="INFO")

    db_host: str = Field(default="localhost")
    db_port: int = Field(default=5432)
    db_name: str = Field(default="db_notification")
    db_user: str = Field(default="postgres")
    db_password: str = Field(default="postgres")
    db_pool_size: int = Field(default=10)
    db_max_overflow: int = Field(default=20)

    @property
    def database_dsn(self) -> str:
        return (
            f"postgresql+asyncpg://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
