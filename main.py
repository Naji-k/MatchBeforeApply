import asyncio
import json
import os

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

from agents.orchestrator import root_agent
from tools.pdf_parser import extract_text_from_pdf
from mock import mock, mock2

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
        raise HTTPException(
            status_code=400, detail="PDF appears to be empty or unreadable."
        )

    # Run the agent pipeline
    # session_service = InMemorySessionService()
    # session = await session_service.create_session(
    #     app_name="cv_job_matcher",
    #     user_id="user",
    #     state={
    #         "cv_text": cv_text,
    #         "jd_type": jd_type,
    #         "jd_input": jd_input,
    #     },
    # )

    # runner = Runner(
    #     agent=root_agent,
    #     app_name="cv_job_matcher",
    #     session_service=session_service,
    # )

    # try:
    #     async for event in runner.run_async(
    #         user_id="user",
    #         session_id=session.id,
    #         new_message=Content(parts=[Part(text="Begin analysis.")]),
    #     ):
    #         pass
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=f"Pipeline error: {e}")

    # final_session = await session_service.get_session(
    #     app_name="cv_job_matcher",
    #     user_id="user",
    #     session_id=session.id,
    # )
    state = mock

    def parse_json_field(key: str):
        value = state.get(key, "")
        if not value:
            return {}
        # output_schema agents store a dict or Pydantic model, not a string
        if isinstance(value, dict):
            return value
        if hasattr(value, "model_dump"):
            return value.model_dump()
        # Plain JSON string
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            pass
        # Markdown-wrapped JSON (```json ... ```)
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

    res = {
        "match_result": parse_json_field("match_result"),
        "ats_tips": parse_json_field("ats_tips"),
        "cover_letter": state.get("cover_letter", ""),
    }
    return res


# ── Frontend static file serving ──────────────────────────────────────────────
frontend_path = os.path.join(os.path.dirname(__file__), "frontend")

if os.path.isdir(frontend_path):
    # GET "/" must be registered BEFORE app.mount("/", ...) otherwise
    # the mount at "/" matches first and this route is never reached
    @app.get("/", include_in_schema=False)
    async def serve_index():
        return FileResponse(os.path.join(frontend_path, "index.html"))

    app.mount("/", StaticFiles(directory=frontend_path), name="static")
