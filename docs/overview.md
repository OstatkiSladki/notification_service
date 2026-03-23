# Notification Service: обзор проекта

## 1. Что уже реализовано

Сервис уведомлений теперь собран по слоистой структуре как в `order_service-main`:

- `api/` - HTTP endpoints
- `core/` - конфиг и подключение БД (SQLAlchemy)
- `models/` - ORM-модели таблиц
- `repositories/` - работа с данными
- `services/` - бизнес-логика
- `schemas/` - Pydantic схемы API
- `rpc/` - точка расширения для межсервисных вызовов/публикации событий
- `migrations/` - SQL-миграции для схемы notification
- `tests/` - интеграционные тесты

База данных подключена к PostgreSQL (`db_notification`), таблица
`notification.notifications` поднимается миграцией, а не автоматически на каждом старте.

Также уже реализовано:

- полноценный pipeline `API -> service -> repository -> DB`
- работа через SQLAlchemy Session dependency (`get_db`)
- ORM-сущность `Notification` с полями статуса прочтения и времени
- проверка доступа пользователя по заголовку `X-User-Id`
- интеграционные тесты для основных сценариев
- готовый SQL-файл миграции `001_create_notification_notifications.sql`

## 2. Какие есть эндпоинты

Базовый префикс: `/api/v1`

1. `GET /api/v1/notifications`
- получить список уведомлений пользователя
- query-параметры:
  - `is_read` (boolean, optional)
  - `page` (integer, default `1`)
  - `limit` (integer, default `20`, max `100`)
- ответ: `200` + `NotificationListResponse`

Пример:

```http
GET /api/v1/notifications?is_read=false&page=1&limit=20
```

2. `GET /api/v1/notifications/{notification_id}`
- получить одно уведомление
- ответ:
  - `200` + `NotificationResponse`
  - `404`, если не найдено

Пример:

```http
GET /api/v1/notifications/10
```

3. `PATCH /api/v1/notifications/{notification_id}`
- обновить поля уведомления (`title`, `message`, `data_json`)
- ответ: `200` + `NotificationResponse`

Пример тела запроса:

```json
{
  "title": "Обновленный заголовок",
  "message": "Новый текст уведомления",
  "data_json": {
    "order_id": 55
  }
}
```

4. `DELETE /api/v1/notifications/{notification_id}`
- удалить уведомление
- ответ: `204 No Content`

5. `PATCH /api/v1/notifications/{notification_id}/read`
- отметить одно уведомление как прочитанное
- ответ: `200`

6. `POST /api/v1/notifications/mark-all-read`
- отметить все уведомления пользователя как прочитанные
- ответ: `200`

## 3. Какие schemas используются

Файл: `schemas/notifications.py`

1. `NotificationResponse`
- одно уведомление в ответе API
- поля: `id`, `user_id`, `type`, `title`, `message`, `data_json`, `is_read`, `created_at`, `read_at`

2. `NotificationListResponse`
- ответ со списком уведомлений
- поля: `items`, `total`, `page`, `limit`

3. `UpdateNotificationRequest`
- тело запроса для обновления уведомления
- поля: `title`, `message`, `data_json`

## 4. Как это работает (простыми словами)

- `main.py` создает FastAPI-приложение.
- В приложение подключается роутер из `api/router.py`.
- Роутер `api/notifications.py` описывает URL, параметры и коды ответов.
- Pydantic-схемы проверяют входящие/исходящие данные.
- Настройки (`host`, `port`, префикс API и т.д.) берутся из env через `core/config.py`.
- Доступ к данным идет через `core/database.py` -> `repositories/notifications.py`.
- Бизнес-правила лежат в `services/notifications.py`.

Сейчас endpoint-ы не являются заглушками: операции списка, чтения, обновления, удаления и отметки прочитанности выполняются через сервисный и репозиторный слои с записью в БД.

## 5. Что реализовано в бизнес-логике

Все endpoint-ы уведомлений работают с БД:

- список уведомлений с фильтрацией и пагинацией
- получение одного уведомления
- обновление уведомления
- удаление уведомления
- отметка одного уведомления как прочитанного
- отметка всех уведомлений пользователя как прочитанных

Для запросов используется заголовок `X-User-Id` (временный простой способ идентификации пользователя).

## 6. Что проверить при запуске

1. Применить миграцию из `migrations/001_create_notification_notifications.sql`.
2. Указать `DATABASE_URL` в `.env`.
3. Запустить сервис и открыть `/docs`.
4. Выполнить запросы к endpoint-ам уведомлений с заголовком `X-User-Id`.
