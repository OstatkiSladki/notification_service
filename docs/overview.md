# Notification Service: обзор проекта

## 1. Что уже реализовано

Сейчас в проекте готов базовый каркас сервиса уведомлений:

- поднято FastAPI-приложение (`main.py`)
- подключен роутер с endpoint-ами уведомлений
- добавлены Pydantic-схемы для запросов и ответов
- сделан конфиг через переменные окружения (`core/config.py`)
- добавлена OpenAPI security-схема `CookieAuth` (cookie `access_token`)

Важно: бизнес-логики пока нет. Это нормально для текущего этапа.

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

То есть сейчас API уже "видно" в Swagger и контракты готовы, но внутри endpoint-ов пока нет реальной работы с БД или очередями.

## 5. Какие части пока заглушки

В каждом endpoint-е пока стоит:

```python
raise NotImplementedError(...)
```

Это значит, что:
- маршруты и валидация уже готовы
- но реальная логика (получение, обновление, удаление уведомлений) будет добавляться на следующем этапе

Пример следующего шага:
- в `GET /api/v1/notifications` вместо заглушки вернуть тестовый список из 1-2 объектов
- затем подключить репозиторий/БД
