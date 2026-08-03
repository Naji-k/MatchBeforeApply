import logging
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import ProgrammingError

load_dotenv()

from api.routes.applications import router as applications_router  # noqa: E402
from api.routes.auth import router as auth_router  # noqa: E402
from api.routes.faq import router as faq_router  # noqa: E402
from api.routes.feedback import router as feedback_router  # noqa: E402
from api.routes.profile import router as profile_router  # noqa: E402
from core.config import settings  # noqa: E402
from db.database import SessionLocal  # noqa: E402
from services.faq_index_service import FaqParseError, index_faq  # noqa: E402

logger = logging.getLogger(__name__)


async def startup_index_faq() -> None:
    """Bring faq_chunks in line with the markdown corpus.

    Failure handling is deliberately asymmetric. entrypoint.sh holds Caddy behind
    a /api/config healthcheck, so anything that blocks this lifespan takes the
    whole site down -- login included. A malformed corpus is our bug and should
    stop the deploy; a Gemini outage is someone else's and must not cost the app
    its uptime for its least important feature.
    """
    async with SessionLocal() as db:
        try:
            logger.info("%s", await index_faq(db))
        except FaqParseError:
            raise
        except ProgrammingError as exc:
            if "faq_chunks" in str(exc):
                logger.error(
                    "faq_chunks missing -- this database has no pgvector. Install it, "
                    "then run `alembic downgrade -1 && alembic upgrade head`. "
                    "FAQ chat will refuse every question until then."
                )
            else:
                logger.exception("FAQ indexing failed on a database error")
        except Exception:
            logger.exception("FAQ indexing failed; chat will refuse until next deploy")


@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.ENABLE_FAQ_CHAT:
        await startup_index_faq()
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
app.include_router(faq_router)
