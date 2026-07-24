import pytest
from fastapi import HTTPException

from conftest import make_result
from db.models import ApplicationComment, CommentType


@pytest.mark.asyncio
async def test_create_application_runs_analysis_immediately(
    authed_client, mock_db, mocker, mock_application
):
    mock_application.match_score = 7
    mocker.patch(
        "services.application_service._run_and_persist_analysis",
        return_value=mock_application,
    )

    response = await authed_client.post(
        "/api/applications",
        json={
            "jd_source": "A job posting",
            "jd_type": "text",
            "jd_text": "A job posting",
            "run_analysis": True,
        },
    )

    assert response.status_code == 201
    assert response.json()["match_score"] == 7


@pytest.mark.asyncio
async def test_list_applications_returns_only_current_users_rows(
    authed_client, mock_db, mock_application
):
    mock_db.execute.return_value = make_result(scalars_list=[mock_application])

    response = await authed_client.get("/api/applications")

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["user_id"] == mock_application.user_id


@pytest.mark.asyncio
async def test_get_application_not_found_returns_404(authed_client, mock_db):
    mock_db.execute.return_value = make_result(scalar=None)

    response = await authed_client.get("/api/applications/999")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_patch_application_updates_status(
    authed_client, mock_db, mock_application
):
    mock_db.execute.return_value = make_result(scalar=mock_application)

    response = await authed_client.patch(
        f"/api/applications/{mock_application.id}", json={"status": "accepted"}
    )

    assert response.status_code == 200
    assert response.json()["status"] == "accepted"


@pytest.mark.asyncio
async def test_delete_application_returns_204(authed_client, mock_db, mock_application):
    mock_db.execute.return_value = make_result(scalar=mock_application)

    response = await authed_client.delete(f"/api/applications/{mock_application.id}")

    assert response.status_code == 204
    mock_db.delete.assert_awaited_once_with(mock_application)


@pytest.mark.asyncio
async def test_add_and_return_comment(authed_client, mock_db, mock_application):
    mock_db.execute.return_value = make_result(scalar=mock_application)

    response = await authed_client.post(
        f"/api/applications/{mock_application.id}/comments",
        json={"type": "general", "comment": "Left a great impression"},
    )

    assert response.status_code == 201
    assert response.json()["comment"] == "Left a great impression"


@pytest.mark.asyncio
async def test_delete_comment_returns_204(authed_client, mock_db, mock_application):
    comment = ApplicationComment(
        id=5,
        application_id=mock_application.id,
        user_id=mock_application.user_id,
        type=CommentType.general,
        comment="note",
    )
    mock_db.execute.side_effect = [
        make_result(scalar=mock_application),  # ownership check
        make_result(scalar=comment),  # comment lookup
    ]

    response = await authed_client.delete(
        f"/api/applications/{mock_application.id}/comments/{comment.id}"
    )

    assert response.status_code == 204


@pytest.mark.asyncio
async def test_unauthenticated_request_returns_401(client):
    response = await client.get("/api/applications")

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_trigger_analyze_returns_429_when_daily_limit_reached(
    authed_client, mock_db, mocker, mock_application
):
    mocker.patch(
        "services.application_service._run_and_persist_analysis",
        side_effect=HTTPException(
            status_code=429,
            detail="Daily analysis limit reached (3/day). Try again tomorrow.",
        ),
    )
    mock_db.execute.return_value = make_result(scalar=mock_application)

    response = await authed_client.post(
        f"/api/applications/{mock_application.id}/analyze"
    )

    assert response.status_code == 429
