from datetime import datetime, timedelta

import pytest
from fastapi import HTTPException

from conftest import make_result
from core.security import verify_password
from schemas.auth import UserCreate
from services.auth_service import (
    authenticate_user,
    generate_and_save_otp,
    google_auth_user,
    register_user,
    verify_otp_code,
)


@pytest.mark.asyncio
async def test_register_user_creates_and_sends_otp(mock_db, mocker):
    mock_db.execute.return_value = make_result(scalar=None)  # no existing user
    send_otp = mocker.patch("services.email_service.send_otp_email")

    user = await register_user(
        mock_db,
        UserCreate(email="new@example.com", password="s3cret!", full_name="New User"),
    )

    assert user.email == "new@example.com"
    assert user.is_email_verified is False
    assert verify_password("s3cret!", user.hashed_password) is True
    mock_db.add.assert_called_once()
    send_otp.assert_called_once()
    assert send_otp.call_args.args[0] == "new@example.com"


@pytest.mark.asyncio
async def test_register_user_rejects_duplicate_email(mock_db, mock_user):
    mock_db.execute.return_value = make_result(scalar=mock_user)

    with pytest.raises(HTTPException) as exc_info:
        await register_user(mock_db, UserCreate(email=mock_user.email, password="x"))

    assert exc_info.value.status_code == 400
    mock_db.add.assert_not_called()


@pytest.mark.asyncio
async def test_authenticate_user_accepts_correct_password(mock_db, mock_user):
    mock_db.execute.return_value = make_result(scalar=mock_user)

    user = await authenticate_user(mock_db, mock_user.email, "correct-password")

    assert user is not None
    assert user.id == mock_user.id


@pytest.mark.asyncio
async def test_authenticate_user_rejects_wrong_password(mock_db, mock_user):
    mock_db.execute.return_value = make_result(scalar=mock_user)

    user = await authenticate_user(mock_db, mock_user.email, "wrong-password")

    assert user is None


@pytest.mark.asyncio
async def test_authenticate_user_rejects_unknown_email(mock_db):
    mock_db.execute.return_value = make_result(scalar=None)

    user = await authenticate_user(mock_db, "nobody@example.com", "whatever")

    assert user is None


@pytest.mark.asyncio
async def test_generate_and_save_otp_sets_code_and_expiry(mock_db, mock_user):
    otp = await generate_and_save_otp(mock_db, mock_user)

    assert len(otp) == 6
    assert otp.isdigit()
    assert mock_user.otp_code == otp
    assert mock_user.otp_expires_at is not None
    mock_db.commit.assert_awaited()


@pytest.mark.asyncio
async def test_verify_otp_code_accepts_correct_unexpired_code(mock_db, mock_user):
    mock_user.otp_code = "123456"
    mock_user.otp_expires_at = datetime.utcnow() + timedelta(minutes=5)

    ok = await verify_otp_code(mock_db, mock_user, "123456")

    assert ok is True
    assert mock_user.is_email_verified is True
    assert mock_user.otp_code is None


@pytest.mark.asyncio
async def test_verify_otp_code_rejects_expired_code(mock_db, mock_user):
    mock_user.is_email_verified = False
    mock_user.otp_code = "123456"
    mock_user.otp_expires_at = datetime.utcnow() - timedelta(minutes=1)

    ok = await verify_otp_code(mock_db, mock_user, "123456")

    assert ok is False
    assert mock_user.is_email_verified is False


@pytest.mark.asyncio
async def test_verify_otp_code_rejects_wrong_code(mock_db, mock_user):
    mock_user.otp_code = "123456"
    mock_user.otp_expires_at = datetime.utcnow() + timedelta(minutes=5)

    ok = await verify_otp_code(mock_db, mock_user, "000000")

    assert ok is False


@pytest.mark.asyncio
async def test_google_auth_user_links_existing_email_account(mock_db, mock_user):
    mock_db.execute.side_effect = [
        make_result(scalar=None),  # lookup by google_id -> none
        make_result(scalar=mock_user),  # lookup by email -> existing local user
    ]

    user = await google_auth_user(mock_db, "google-123", mock_user.email, "Jane Doe")

    assert user.id == mock_user.id
    assert user.google_id == "google-123"
    assert user.auth_provider == "google"


@pytest.mark.asyncio
async def test_google_auth_user_creates_new_user_when_no_match(mock_db):
    mock_db.execute.side_effect = [
        make_result(scalar=None),  # lookup by google_id -> none
        make_result(scalar=None),  # lookup by email -> none
    ]

    user = await google_auth_user(
        mock_db, "google-999", "brandnew@example.com", "Brand New"
    )

    assert user.email == "brandnew@example.com"
    assert user.google_id == "google-999"
    assert user.is_email_verified is True
    mock_db.add.assert_called_once()
