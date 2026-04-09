import json

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part
from agents.orchestrator import root_agent
from fastapi import HTTPException

from core.config import settings

from services.mock_data import mock


def parse_json_field(state: dict, key: str):
    value = state.get(key, "")
    if not value:
        return {}
    if isinstance(value, dict):
        return value
    if hasattr(value, "model_dump"):
        return value.model_dump()
    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError):
        pass
    if isinstance(value, str):
        clean = value.strip()
        if clean.startswith("```"):
            lines = clean.splitlines()
            clean = "\n".join(lines[1:-1])
        try:
            return json.loads(clean)
        except (json.JSONDecodeError, ValueError):
            pass
    return {}


async def run_analysis(cv_text: str, jd_type: str, jd_input: str, user_id: int) -> dict:
    # Run the agent pipeline
    if settings.is_production:
        session_service = InMemorySessionService()
        session = await session_service.create_session(
            app_name="cv_job_matcher",
            user_id=str(user_id),
            state={
                "cv_text": cv_text,
                "jd_type": jd_type,
                "jd_input": jd_input,
            },
        )

        runner = Runner(
            agent=root_agent,
            app_name="cv_job_matcher",
            session_service=session_service,
        )

        try:
            async for event in runner.run_async(
                user_id=str(user_id),
                session_id=session.id,
                new_message=Content(
                    parts=[Part(text=f"jd_type: {jd_type}\n\n{jd_input}")]
                ),
            ):
                pass
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Pipeline error: {e}")

        final_session = await session_service.get_session(
            app_name="cv_job_matcher",
            user_id=str(user_id),
            session_id=session.id,
        )
        state = final_session.state
    else:
        # In development, return mock data without running the pipeline
        state = mock

    return {
        "match_result": parse_json_field(state, "match_result"),
        "ats_tips": parse_json_field(state, "ats_tips"),
        "jd_data": parse_json_field(state, "jd_data"),
        "cv_data": parse_json_field(state, "cv_data"),
    }
