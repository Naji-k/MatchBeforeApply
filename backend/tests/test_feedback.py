import pytest

from tests.conftest import make_result


# Uses `client` + real auth_headers rather than `authed_client`: the route reads
# the Authorization header itself, so the dependency override in `authed_client`
# would not reach it and every case would look anonymous.
@pytest.mark.asyncio
async def test_submit_feedback_attributes_a_logged_in_user(
    client, mock_db, mock_user, auth_headers, mocker
):
    mock_db.execute.return_value = make_result(scalar=mock_user)
    send_email = mocker.patch("api.routes.feedback.send_feedback_email")

    response = await client.post(
        "/api/feedback", json={"message": "Love the product!"}, headers=auth_headers
    )

    assert response.status_code == 204
    send_email.assert_called_once()
    _, kwargs = send_email.call_args
    assert kwargs["message"] == "Love the product!"
    assert kwargs["user_name"] == "Jane Doe"
    assert kwargs["user_email"] == "jane@example.com"


@pytest.mark.asyncio
async def test_submit_feedback_accepts_anonymous(client, mocker):
    """The FAQ chat widget is unauthenticated, so this must not 401."""
    send_email = mocker.patch("api.routes.feedback.send_feedback_email")

    response = await client.post("/api/feedback", json={"message": "hi"})

    assert response.status_code == 204
    _, kwargs = send_email.call_args
    assert kwargs["user_name"] == "Anonymous"
    assert kwargs["user_email"] == ""


@pytest.mark.asyncio
async def test_submit_feedback_treats_a_bad_token_as_anonymous(client, mocker):
    """A stale token should still deliver the feedback, just unattributed."""
    send_email = mocker.patch("api.routes.feedback.send_feedback_email")

    response = await client.post(
        "/api/feedback",
        json={"message": "hi"},
        headers={"Authorization": "Bearer not-a-real-jwt"},
    )

    assert response.status_code == 204
    _, kwargs = send_email.call_args
    assert kwargs["user_name"] == "Anonymous"


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
