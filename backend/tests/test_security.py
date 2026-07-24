from datetime import timedelta

from jose import jwt

from core.config import settings
from core.security import ALGORITHM, create_access_token, hash_password, verify_password


def test_hash_password_produces_a_verifiable_but_different_hash():
    hashed = hash_password("s3cret!")
    assert hashed != "s3cret!"
    assert verify_password("s3cret!", hashed) is True


def test_verify_password_rejects_wrong_password():
    hashed = hash_password("s3cret!")
    assert verify_password("wrong-password", hashed) is False


def test_create_access_token_encodes_subject_and_expiry():
    token = create_access_token(data={"sub": "42"}, expires_delta=timedelta(minutes=5))
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
    assert payload["sub"] == "42"
    assert "exp" in payload


def test_create_access_token_uses_default_expiry_when_not_given():
    token = create_access_token(data={"sub": "42"})
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
    assert payload["sub"] == "42"
