import pytest


@pytest.mark.asyncio
async def test_get_notifications_empty(client, user_headers):
    response = await client.get("/api/v1/notifications", headers=user_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []
    assert data["total"] == 0


@pytest.mark.asyncio
async def test_get_notification_by_id(client, user_headers, seed_notification):
    response = await client.get(f"/api/v1/notifications/{seed_notification}", headers=user_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == seed_notification
    assert data["user_id"] == 1


@pytest.mark.asyncio
async def test_get_notification_forbidden_for_other_user(
    client, another_user_headers, seed_notification
):
    response = await client.get(
        f"/api/v1/notifications/{seed_notification}", headers=another_user_headers
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_notification(client, user_headers, seed_notification):
    payload = {"title": "Новый заголовок", "message": "Новый текст"}
    response = await client.patch(
        f"/api/v1/notifications/{seed_notification}", json=payload, headers=user_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Новый заголовок"
    assert data["message"] == "Новый текст"


@pytest.mark.asyncio
async def test_mark_notification_read(client, user_headers, seed_notification):
    response = await client.patch(
        f"/api/v1/notifications/{seed_notification}/read", headers=user_headers
    )
    assert response.status_code == 200

    check_response = await client.get(
        f"/api/v1/notifications/{seed_notification}", headers=user_headers
    )
    data = check_response.json()
    assert data["is_read"] is True
    assert data["read_at"] is not None


@pytest.mark.asyncio
async def test_mark_all_notifications_read(client, user_headers, seed_notification):
    response = await client.post("/api/v1/notifications/mark-all-read", headers=user_headers)
    assert response.status_code == 200

    check_response = await client.get(
        f"/api/v1/notifications/{seed_notification}", headers=user_headers
    )
    assert check_response.status_code == 200
    assert check_response.json()["is_read"] is True


@pytest.mark.asyncio
async def test_delete_notification(client, user_headers, seed_notification):
    delete_response = await client.delete(
        f"/api/v1/notifications/{seed_notification}", headers=user_headers
    )
    assert delete_response.status_code == 204

    get_response = await client.get(
        f"/api/v1/notifications/{seed_notification}", headers=user_headers
    )
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_missing_user_header(client):
    response = await client.get("/api/v1/notifications")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_invalid_user_header(client):
    response = await client.get("/api/v1/notifications", headers={"X-User-ID": "abc"})
    assert response.status_code == 422
