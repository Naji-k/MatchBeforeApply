import pytest


@pytest.mark.asyncio
async def test_submit_feedback_schedules_email_and_returns_204(authed_client, mocker):
    send_email = mocker.patch("api.routes.feedback.send_feedback_email")

    response = await authed_client.post(
        "/api/feedback", json={"message": "Love the product!"}
    )

    assert response.status_code == 204
    send_email.assert_called_once()
    _, kwargs = send_email.call_args
    assert kwargs["message"] == "Love the product!"


@pytest.mark.asyncio
async def test_submit_feedback_requires_auth(client):
    response = await client.post("/api/feedback", json={"message": "hi"})

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_config_returns_public_settings(client):
    response = await client.get("/api/config")

    assert response.status_code == 200
    body = response.json()
    assert "VITE_GOOGLE_CLIENT_ID" in body
    assert "VITE_ENABLE_SIGNUP" in body


@pytest.mark.asyncio
async def test_config_exposes_faq_chat_flag(client):
    response = await client.get("/api/config")
    assert response.status_code == 200
    assert response.json()["ENABLE_FAQ_CHAT"] is False
