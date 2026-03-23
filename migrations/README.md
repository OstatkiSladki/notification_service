# Migrations

В этой папке лежат SQL-миграции для сервиса уведомлений.

Миграция `001_create_notification_notifications.sql` создает схему
`notification` и таблицу `notifications`.

Пример применения (PostgreSQL):

```bash
psql "$DATABASE_URL" -f migrations/001_create_notification_notifications.sql
```
