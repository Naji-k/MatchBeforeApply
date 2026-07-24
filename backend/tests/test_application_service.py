import pytest
from fastapi import HTTPException

from conftest import make_result
from db.models import ApplicationComment, ApplicationStatus, CommentType
from schemas.application import ApplicationCreate, ApplicationUpdate, CommentCreate
from services.application_service import (
    create_application,
    create_comment,
    delete_application,
    delete_comment,
    get_application,
    list_applications,
    list_comments,
    update_application,
)


@pytest.mark.asyncio
async def test_list_applications_returns_only_that_users_rows(
    mock_db, mock_application
):
    mock_db.execute.return_value = make_result(scalars_list=[mock_application])

    apps = await list_applications(mock_db, mock_application.user_id)

    assert apps == [mock_application]


@pytest.mark.asyncio
async def test_get_application_raises_404_when_not_owned_or_missing(mock_db):
    mock_db.execute.return_value = make_result(scalar=None)

    with pytest.raises(HTTPException) as exc_info:
        await get_application(mock_db, user_id=1, application_id=999)

    assert exc_info.value.status_code == 404


@pytest.mark.asyncio
async def test_create_application_without_analysis_skips_pipeline(mock_db, mocker):
    run_analysis = mocker.patch(
        "services.application_service._run_and_persist_analysis"
    )

    app = await create_application(
        mock_db,
        user_id=1,
        data=ApplicationCreate(
            jd_source="A job", jd_type="text", jd_text="A job", run_analysis=False
        ),
    )

    assert app.jd_source == "A job"
    run_analysis.assert_not_called()
    mock_db.add.assert_called_once()


@pytest.mark.asyncio
async def test_create_application_with_analysis_runs_pipeline(
    mock_db, mocker, mock_application
):
    mock_application.match_score = 8
    mocker.patch(
        "services.application_service._run_and_persist_analysis",
        return_value=mock_application,
    )

    app = await create_application(
        mock_db,
        user_id=1,
        data=ApplicationCreate(
            jd_source="A job", jd_type="text", jd_text="A job", run_analysis=True
        ),
    )

    assert app.match_score == 8


@pytest.mark.asyncio
async def test_update_application_patches_only_provided_fields(
    mock_db, mock_application
):
    mock_db.execute.return_value = make_result(scalar=mock_application)

    updated = await update_application(
        mock_db,
        mock_application.user_id,
        mock_application.id,
        ApplicationUpdate(status=ApplicationStatus.accepted),
    )

    assert updated.status == ApplicationStatus.accepted
    assert updated.jd_source == mock_application.jd_source  # untouched


@pytest.mark.asyncio
async def test_delete_application_deletes_the_row(mock_db, mock_application):
    # ApplicationComment rows cascade via the ORM relationship's
    # cascade="all, delete-orphan" (db/models.py); with a mocked session we
    # can only assert delete() is invoked on the parent, not that rows vanish.
    mock_db.execute.return_value = make_result(scalar=mock_application)

    await delete_application(mock_db, mock_application.user_id, mock_application.id)

    mock_db.delete.assert_awaited_once_with(mock_application)
    mock_db.commit.assert_awaited()


@pytest.mark.asyncio
async def test_list_comments_returns_applications_comments(mock_db, mock_application):
    comment = ApplicationComment(
        id=1,
        application_id=mock_application.id,
        user_id=mock_application.user_id,
        type=CommentType.general,
        comment="Good culture fit",
    )
    mock_db.execute.side_effect = [
        make_result(scalar=mock_application),  # get_application ownership check
        make_result(scalars_list=[comment]),  # comments query
    ]

    comments = await list_comments(
        mock_db, mock_application.user_id, mock_application.id
    )

    assert comments == [comment]


@pytest.mark.asyncio
async def test_create_comment_adds_comment_to_owned_application(
    mock_db, mock_application
):
    mock_db.execute.return_value = make_result(scalar=mock_application)

    comment = await create_comment(
        mock_db,
        mock_application.user_id,
        mock_application.id,
        CommentCreate(
            type=CommentType.qa, question="Salary range?", comment="Asked in screen"
        ),
    )

    assert comment.comment == "Asked in screen"
    mock_db.add.assert_called_once()


@pytest.mark.asyncio
async def test_delete_comment_raises_404_when_comment_not_found(
    mock_db, mock_application
):
    mock_db.execute.side_effect = [
        make_result(scalar=mock_application),  # ownership check
        make_result(scalar=None),  # comment lookup
    ]

    with pytest.raises(HTTPException) as exc_info:
        await delete_comment(
            mock_db, mock_application.user_id, mock_application.id, comment_id=555
        )

    assert exc_info.value.status_code == 404
