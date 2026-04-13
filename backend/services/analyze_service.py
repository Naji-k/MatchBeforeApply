import asyncio
import json
from typing import AsyncGenerator

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part
from agents.orchestrator import root_agent

from core.config import settings
from services.mock_data import mock, mock2, mock3
import random

AGENT_STEPS: dict[str, tuple[int, str]] = {
    "jd_agent": (0, "Reading job description"),
    "cv_agent": (1, "Parsing your CV"),
    "match_agent": (2, "Scoring the match"),
    "ats_agent": (3, "Generating match insights"),
}


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


async def stream_analysis(
    cv_text: str, jd_type: str, jd_input: str, user_id: int
) -> AsyncGenerator[dict, None]:
    if not settings.is_production or user_id == settings.DEMO_USER:
        random_mock = random.choice([mock, mock2, mock3])
        for agent, (step, label) in AGENT_STEPS.items():
            yield {"type": "step_start", "step": step, "agent": agent, "label": label}
            await asyncio.sleep(0.5)
            yield {"type": "step_done", "step": step, "agent": agent}
        yield {"type": "_state", "state": random_mock}
        return

    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name="cv_job_matcher",
        user_id=str(user_id),
        state={"cv_text": cv_text, "jd_type": jd_type, "jd_input": jd_input},
    )
    runner = Runner(
        agent=root_agent,
        app_name="cv_job_matcher",
        session_service=session_service,
    )
    current_author = None

    try:
        async for event in runner.run_async(
            user_id=str(user_id),
            session_id=session.id,
            new_message=Content(parts=[Part(text=f"jd_type: {jd_type}\n\n{jd_input}")]),
        ):
            author = event.author
            if not author or author == "user":
                continue
            if author in AGENT_STEPS and author != current_author:
                if current_author in AGENT_STEPS:
                    yield {
                        "type": "step_done",
                        "step": AGENT_STEPS[current_author][0],
                        "agent": current_author,
                    }
                current_author = author
                step, label = AGENT_STEPS[author]
                yield {
                    "type": "step_start",
                    "step": step,
                    "agent": author,
                    "label": label,
                }
            if event.is_final_response() and author in AGENT_STEPS:
                yield {
                    "type": "step_done",
                    "step": AGENT_STEPS[author][0],
                    "agent": author,
                }
                current_author = None
    except Exception as e:
        yield {"type": "error", "message": f"Pipeline error: {e}"}
        return

    final_session = await session_service.get_session(
        app_name="cv_job_matcher",
        user_id=str(user_id),
        session_id=session.id,
    )
    yield {"type": "_state", "state": final_session.state}
