# Migrations

Актуальные миграции выполняются через Alembic.

Основные команды:

```bash
uv run alembic upgrade head
uv run alembic downgrade -1
```

Файл `001_create_notification_notifications.sql` оставлен как исторический артефакт.
