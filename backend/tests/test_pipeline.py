from unittest.mock import AsyncMock

import pytest
from fastapi import HTTPException

from conftest import make_result
from core.config import settings
from services import mock_data
from services.analyze_service import stream_analysis
from services.application_service import (
    analyze_application,
    stream_and_persist_analysis,
)
from services.limit_service import DAILY_ANALYSIS_LIMIT

REQUIRED_MATCH_FIELDS = {
    "overall_score",
    "skills_score",
    "matched_skills",
    "missing_skills",
    "summary",
}


@pytest.mark.asyncio
async def test_stream_analysis_dev_mode_returns_mock_pipeline_shape(mocker):
    mocker.patch.object(settings, "ENV", "development")
    mocker.patch("services.analyze_service.asyncio.sleep", new=AsyncMock())

    events = [
        event async for event in stream_analysis("cv text", "text", "a job", user_id=1)
    ]

    step_events = [e for e in events if e["type"] in ("step_start", "step_done")]
    assert len(step_events) == 8  # 4 agents x start/done

    state_event = events[-1]
    assert state_event["type"] == "_state"
    match_result = state_event["state"]["match_result"]
    assert REQUIRED_MATCH_FIELDS.issubset(match_result.keys())


@pytest.mark.asyncio
async def test_stream_analysis_production_mode_drives_the_adk_runner(mocker):
    mocker.patch.object(settings, "ENV", "production")

    fake_event = mocker.MagicMock()
    fake_event.author = "jd_agent"
    fake_event.is_final_response.return_value = True

    async def fake_run_async(**kwargs):
        yield fake_event

    fake_session = mocker.MagicMock()
    fake_session.id = "session-1"
    fake_session.state = {"match_result": {}, "ats_tips": {}, "jd_data": {}}

    session_service = mocker.MagicMock()
    session_service.create_session = AsyncMock(return_value=fake_session)
    session_service.get_session = AsyncMock(return_value=fake_session)
    mocker.patch(
        "services.analyze_service.InMemorySessionService", return_value=session_service
    )

    runner = mocker.MagicMock()
    runner.run_async = fake_run_async
    mocker.patch("services.analyze_service.Runner", return_value=runner)

    events = [
        event async for event in stream_analysis("cv text", "text", "a job", user_id=1)
    ]

    assert events[-1]["type"] == "_state"
    assert events[-1]["state"] == fake_session.state


@pytest.mark.asyncio
async def test_stream_and_persist_analysis_persists_match_result_on_application(
    mock_db, mock_user, mock_application, mock_profile, mocker
):
    async def fake_stream_analysis(cv_text, jd_type, jd_input, user_id):
        yield {
            "type": "step_start",
            "step": 0,
            "agent": "jd_agent",
            "label": "Reading job description",
        }
        yield {"type": "_state", "state": mock_data.mock}

    mocker.patch(
        "services.application_service.stream_analysis", side_effect=fake_stream_analysis
    )
    mock_db.execute.side_effect = [
        make_result(scalar=mock_user),  # user lookup (email-verification check)
        make_result(scalar=mock_application),  # get_application ownership check
        make_result(scalar=mock_profile),  # get_or_create_profile (cv_text check)
        make_result(
            scalar=mock_profile
        ),  # get_or_create_profile again, inside the limit check
    ]

    events = [
        event
        async for event in stream_and_persist_analysis(
            mock_db, mock_user.id, mock_application.id
        )
    ]

    assert events[-1]["type"] == "done"
    assert (
        mock_application.match_score == mock_data.mock["match_result"]["overall_score"]
    )
    assert mock_application.match_breakdown == mock_data.mock["match_result"]
    assert mock_application.ats_tips == mock_data.mock["ats_tips"]
    assert mock_application.jd_data == mock_data.mock["jd_data"]


@pytest.mark.asyncio
async def test_stream_and_persist_analysis_blocks_unverified_email(
    mock_db, mock_user, mock_application
):
    mock_user.is_email_verified = False
    mock_db.execute.return_value = make_result(scalar=mock_user)

    events = [
        event
        async for event in stream_and_persist_analysis(
            mock_db, mock_user.id, mock_application.id
        )
    ]

    assert len(events) == 1
    assert events[0]["type"] == "error"
    assert events[0]["status_code"] == 403


@pytest.mark.asyncio
async def test_stream_and_persist_analysis_errors_without_a_cv(
    mock_db, mock_user, mock_application, mock_profile
):
    mock_profile.cv_text = None
    mock_db.execute.side_effect = [
        make_result(scalar=mock_user),
        make_result(scalar=mock_application),
        make_result(scalar=mock_profile),
    ]

    events = [
        event
        async for event in stream_and_persist_analysis(
            mock_db, mock_user.id, mock_application.id
        )
    ]

    assert events[0]["type"] == "error"
    assert "Upload your CV" in events[0]["message"]


@pytest.mark.asyncio
async def test_analyze_application_raises_429_when_daily_limit_exceeded(
    mock_db, mock_user, mock_application, mock_profile
):
    mock_profile.daily_analyses_used = DAILY_ANALYSIS_LIMIT
    # Call order: analyze_application's own get_application, then inside
    # stream_and_persist_analysis: user lookup, get_application again,
    # get_or_create_profile, and get_or_create_profile again for the limit check.
    mock_db.execute.side_effect = [
        make_result(scalar=mock_application),
        make_result(scalar=mock_user),
        make_result(scalar=mock_application),
        make_result(scalar=mock_profile),
        make_result(scalar=mock_profile),
    ]

    with pytest.raises(HTTPException) as exc_info:
        await analyze_application(mock_db, mock_user.id, mock_application.id)

    assert exc_info.value.status_code == 429
