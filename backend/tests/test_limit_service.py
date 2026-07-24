from datetime import date, timedelta

import pytest
from fastapi import HTTPException

from conftest import make_result
from core.config import settings
from services.limit_service import DAILY_ANALYSIS_LIMIT, check_and_increment_daily_limit


@pytest.mark.asyncio
async def test_increments_usage_within_limit(mock_db, mock_profile):
    mock_profile.daily_analyses_used = 0
    mock_profile.daily_analyses_reset_date = date.today()
    mock_db.execute.return_value = make_result(scalar=mock_profile)

    await check_and_increment_daily_limit(mock_profile.user_id, mock_db)

    assert mock_profile.daily_analyses_used == 1
    mock_db.commit.assert_awaited()


@pytest.mark.asyncio
async def test_resets_usage_on_a_new_day(mock_db, mock_profile):
    mock_profile.daily_analyses_used = DAILY_ANALYSIS_LIMIT
    mock_profile.daily_analyses_reset_date = date.today() - timedelta(days=1)
    mock_db.execute.return_value = make_result(scalar=mock_profile)

    await check_and_increment_daily_limit(mock_profile.user_id, mock_db)

    assert mock_profile.daily_analyses_reset_date == date.today()
    assert mock_profile.daily_analyses_used == 1


@pytest.mark.asyncio
async def test_raises_429_once_limit_reached(mock_db, mock_profile):
    mock_profile.daily_analyses_used = DAILY_ANALYSIS_LIMIT
    mock_profile.daily_analyses_reset_date = date.today()
    mock_db.execute.return_value = make_result(scalar=mock_profile)

    with pytest.raises(HTTPException) as exc_info:
        await check_and_increment_daily_limit(mock_profile.user_id, mock_db)

    assert exc_info.value.status_code == 429
    assert mock_profile.daily_analyses_used == DAILY_ANALYSIS_LIMIT  # unchanged


@pytest.mark.asyncio
async def test_demo_user_bypasses_the_limit(mock_db, mock_profile, mocker):
    mocker.patch.object(settings, "DEMO_USER", mock_profile.user_id)
    mock_profile.daily_analyses_used = DAILY_ANALYSIS_LIMIT
    mock_db.execute.return_value = make_result(scalar=mock_profile)

    await check_and_increment_daily_limit(mock_profile.user_id, mock_db)

    assert mock_profile.daily_analyses_used == DAILY_ANALYSIS_LIMIT  # untouched
    mock_db.commit.assert_not_awaited()
