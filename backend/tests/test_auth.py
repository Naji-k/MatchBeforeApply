from datetime import datetime

import pytest
from jose import jwt

from conftest import make_result
from core.config import settings
from core.security import ALGORITHM, hash_password
from db.models import User


@pytest.mark.asyncio
async def test_register_returns_201_and_user_payload(client, mock_db, mocker):
    mock_db.execute.return_value = make_result(scalar=None)
    mocker.patch("services.email_service.send_otp_email")

    response = await client.post(
        "/api/auth/register",
        json={
            "email": "new@example.com",
            "password": "s3cret!",
            "full_name": "New User",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["email"] == "new@example.com"
    assert body["is_email_verified"] is False


@pytest.mark.asyncio
async def test_register_duplicate_email_returns_400(client, mock_db, mock_user):
    mock_db.execute.return_value = make_result(scalar=mock_user)

    response = await client.post(
        "/api/auth/register", json={"email": mock_user.email, "password": "s3cret!"}
    )

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_login_correct_credentials_returns_jwt(client, mock_db, mock_user):
    mock_db.execute.return_value = make_result(scalar=mock_user)

    response = await client.post(
        "/api/auth/login",
        data={"username": mock_user.email, "password": "correct-password"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    payload = jwt.decode(
        body["access_token"], settings.SECRET_KEY, algorithms=[ALGORITHM]
    )
    assert payload["sub"] == str(mock_user.id)


@pytest.mark.asyncio
async def test_login_wrong_password_returns_401(client, mock_db, mock_user):
    mock_db.execute.return_value = make_result(scalar=mock_user)

    response = await client.post(
        "/api/auth/login",
        data={"username": mock_user.email, "password": "wrong-password"},
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_me_with_valid_token_returns_current_user(
    client, mock_db, mock_user, auth_headers
):
    mock_db.execute.return_value = make_result(scalar=mock_user)

    response = await client.get("/api/auth/me", headers=auth_headers)

    assert response.status_code == 200
    assert response.json()["email"] == mock_user.email


@pytest.mark.asyncio
async def test_protected_route_rejects_invalid_jwt(client, mock_db):
    response = await client.get(
        "/api/auth/me", headers={"Authorization": "Bearer not-a-real-jwt"}
    )

    assert response.status_code == 401
    mock_db.execute.assert_not_awaited()


@pytest.mark.asyncio
async def test_protected_route_rejects_missing_token(client):
    response = await client.get("/api/auth/me")

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_google_login_returns_503_when_not_configured(client, mocker):
    mocker.patch.object(settings, "GOOGLE_CLIENT_ID", "")

    response = await client.post("/api/auth/google", json={"credential": "whatever"})

    assert response.status_code == 503


@pytest.mark.asyncio
async def test_google_login_invalid_token_returns_401(client, mocker):
    mocker.patch.object(settings, "GOOGLE_CLIENT_ID", "test-client-id")
    mocker.patch(
        "google.oauth2.id_token.verify_oauth2_token",
        side_effect=ValueError("bad token"),
    )

    response = await client.post(
        "/api/auth/google", json={"credential": "bad-credential"}
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_google_login_success_issues_jwt(client, mock_db, mock_user, mocker):
    mocker.patch.object(settings, "GOOGLE_CLIENT_ID", "test-client-id")
    mocker.patch(
        "google.oauth2.id_token.verify_oauth2_token",
        return_value={
            "sub": "google-123",
            "email": mock_user.email,
            "name": mock_user.full_name,
        },
    )
    mocker.patch("api.routes.auth.google_auth_user", return_value=mock_user)

    response = await client.post(
        "/api/auth/google", json={"credential": "fake-credential"}
    )

    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_send_verification_skips_otp_when_already_verified(authed_client, mocker):
    spy = mocker.patch("api.routes.auth.generate_and_save_otp")

    response = await authed_client.post("/api/auth/send-verification")

    assert response.status_code == 204
    spy.assert_not_called()


@pytest.mark.asyncio
async def test_send_verification_sends_otp_when_unverified(
    client, mock_db, mock_user, auth_headers, mocker
):
    mock_user.is_email_verified = False
    mock_db.execute.return_value = make_result(scalar=mock_user)
    mocker.patch("api.routes.auth.generate_and_save_otp", return_value="123456")
    send_email = mocker.patch("api.routes.auth.send_otp_email")

    response = await client.post("/api/auth/send-verification", headers=auth_headers)

    assert response.status_code == 204
    send_email.assert_called_once_with(mock_user.email, "123456")


@pytest.mark.asyncio
async def test_verify_email_wrong_code_returns_400(
    client, mock_db, mock_user, auth_headers, mocker
):
    mock_user.is_email_verified = False
    mock_db.execute.return_value = make_result(scalar=mock_user)
    mocker.patch("api.routes.auth.verify_otp_code", return_value=False)

    response = await client.post(
        "/api/auth/verify-email", json={"code": "000000"}, headers=auth_headers
    )

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_verify_email_correct_code_returns_updated_user(
    client, mock_db, mock_user, auth_headers, mocker
):
    mock_user.is_email_verified = False
    mock_db.execute.return_value = make_result(scalar=mock_user)
    mocker.patch("api.routes.auth.verify_otp_code", return_value=True)

    response = await client.post(
        "/api/auth/verify-email", json={"code": "123456"}, headers=auth_headers
    )

    assert response.status_code == 200
    mock_db.refresh.assert_awaited()


@pytest.mark.asyncio
async def test_demo_login_issues_token_for_demo_user(client, mock_db, mocker):
    demo_user = User(
        id=99,
        email="demo@example.com",
        hashed_password=hash_password("demo-pass"),
        full_name="Demo User",
        is_email_verified=True,
        created_at=datetime(2026, 1, 1),
    )
    mocker.patch.object(settings, "VITE_DEMO_USER_EMAIL", "demo@example.com")
    mocker.patch.object(settings, "VITE_DEMO_USER_PASSWORD", "demo-pass")
    mock_db.execute.return_value = make_result(scalar=demo_user)

    response = await client.post("/api/auth/demo-login")

    assert response.status_code == 200
    assert "access_token" in response.json()
