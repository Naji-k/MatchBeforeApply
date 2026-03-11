import asyncio
import json
import os

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

from agents.orchestrator import root_agent
from tools.pdf_parser import extract_text_from_pdf

app = FastAPI(title="CV ↔ Job Matcher")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/analyze")
async def analyze(
    cv_file: UploadFile = File(...),
    jd_type: str = Form(...),
    jd_input: str = Form(...),
):
    if not os.getenv("GOOGLE_API_KEY"):
        raise HTTPException(status_code=500, detail="GOOGLE_API_KEY not configured.")

    # Extract text from uploaded PDF
    file_bytes = await cv_file.read()
    try:
        cv_text = extract_text_from_pdf(file_bytes)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse PDF: {e}")

    if not cv_text.strip():
        raise HTTPException(status_code=400, detail="PDF appears to be empty or unreadable.")

    # Run the agent pipeline
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name="cv_job_matcher",
        user_id="user",
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
            user_id="user",
            session_id=session.id,
            new_message=Content(parts=[Part(text="Begin analysis.")]),
        ):
            pass
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline error: {e}")

    final_session = await session_service.get_session(
        app_name="cv_job_matcher",
        user_id="user",
        session_id=session.id,
    )

    state = final_session.state

    def parse_json_field(key: str):
        value = state.get(key, "")
        if not value:
            return {}
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return {"raw": value}

    return {
        "match_result": parse_json_field("match_result"),
        "ats_tips": parse_json_field("ats_tips"),

    }


