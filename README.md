# Notification Service

Сервис уведомлений на FastAPI.

## Что делает сервис

- Отдает список уведомлений пользователя
- Отдает одно уведомление по id
- Обновляет уведомление
- Удаляет уведомление
- Отмечает одно уведомление как прочитанное
- Отмечает все уведомления пользователя как прочитанные

## Архитектура

- `api/` - HTTP-роуты
- `core/` - конфиг, база, security-хелперы
- `models/` - SQLAlchemy модели
- `repositories/` - доступ к данным
- `services/` - бизнес-логика
- `schemas/` - Pydantic-схемы
- `rpc/` - точка расширения для интеграции с брокером
- `migrations/` - SQL-миграции
- `tests/` - тесты

## База данных

Основная БД - PostgreSQL.

Используется таблица:

- `notification.notifications`

Миграция:

- `migrations/001_create_notification_notifications.sql`

## Быстрый запуск

1. Установить зависимости:

```bash
pip install -r requirements.txt
```

2. Скопировать `.env.example` в `.env` и выставить корректный `DATABASE_URL`.

3. Применить миграцию:

```bash
psql "$DATABASE_URL" -f migrations/001_create_notification_notifications.sql
```

4. Запустить API:

```bash
uvicorn main:app --host 0.0.0.0 --port 8003 --reload
```

5. Swagger:

- `http://localhost:8003/docs`

## Авторизация

В OpenAPI указан `CookieAuth` (cookie `access_token`).

Для локальной проверки в текущей версии user id берется из заголовка `X-User-Id`.
