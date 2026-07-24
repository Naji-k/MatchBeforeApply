import io
from datetime import date
import pytest
from conftest import make_result


@pytest.mark.asyncio
async def test_get_profile_creates_one_on_first_access(
    authed_client, mock_db, mock_user
):
    mock_db.execute.return_value = make_result(scalar=None)  # no profile yet

    response = await authed_client.get("/api/profile")

    assert response.status_code == 200
    assert response.json()["user_id"] == mock_user.id
    mock_db.add.assert_called_once()


@pytest.mark.asyncio
async def test_get_profile_returns_existing_profile(
    authed_client, mock_db, mock_profile
):
    mock_db.execute.return_value = make_result(scalar=mock_profile)

    response = await authed_client.get("/api/profile")

    assert response.status_code == 200
    assert response.json()["cv_text"] == mock_profile.cv_text


@pytest.mark.asyncio
async def test_get_profile_resets_daily_count_on_new_day(
    authed_client, mock_db, mock_profile
):
    mock_profile.daily_analyses_used = 3
    mock_profile.daily_analyses_reset_date = date(2020, 1, 1)
    mock_db.execute.return_value = make_result(scalar=mock_profile)

    response = await authed_client.get("/api/profile")

    assert response.json()["daily_analyses_used"] == 0


@pytest.mark.asyncio
async def test_put_profile_updates_cv_text(authed_client, mock_db, mock_profile):
    mock_db.execute.return_value = make_result(scalar=mock_profile)

    response = await authed_client.put(
        "/api/profile", json={"cv_text": "Updated CV content"}
    )

    assert response.status_code == 200
    assert response.json()["cv_text"] == "Updated CV content"
    mock_db.commit.assert_awaited()


@pytest.mark.asyncio
async def test_upload_cv_extracts_text_from_pdf(
    authed_client, mock_db, mock_profile, mocker
):
    mock_db.execute.return_value = make_result(scalar=mock_profile)
    mocker.patch(
        "api.routes.profile.extract_text_from_pdf", return_value="Extracted CV text"
    )

    response = await authed_client.post(
        "/api/profile/upload-cv",
        files={
            "cv_file": ("resume.pdf", io.BytesIO(b"%PDF-1.4 fake"), "application/pdf")
        },
    )

    assert response.status_code == 200
    assert response.json()["cv_text"] == "Extracted CV text"
