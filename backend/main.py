from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

from api.routes.applications import router as applications_router  # noqa: E402
from api.routes.auth import router as auth_router  # noqa: E402
from api.routes.profile import router as profile_router  # noqa: E402
from api.routes.feedback import router as feedback_router  # noqa: E402


# Database initialization on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    yield


app = FastAPI(title="CV ↔ Job Matcher", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:8080",
        "https://matchbeforeapply.com",
        "https://www.matchbeforeapply.com",
        "https://matchbeforeapply.up.railway.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(applications_router)
app.include_router(feedback_router)
