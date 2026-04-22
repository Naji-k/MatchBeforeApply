from datetime import datetime
from typing import AsyncGenerator, List

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Application, ApplicationComment, User
from schemas.application import (
    ApplicationCreate,
    ApplicationResponse,
    ApplicationUpdate,
    CommentCreate,
)
from services.analyze_service import parse_json_field, stream_analysis
from services.limit_service import check_and_increment_daily_limit
from services.profile_service import get_or_create_profile


async def list_applications(db: AsyncSession, user_id: int) -> List[Application]:
    result = await db.execute(
        select(Application)
        .where(Application.user_id == user_id)
        .order_by(Application.created_at.desc())
    )
    return list(result.scalars().all())


async def get_application(
    db: AsyncSession, user_id: int, application_id: int
) -> Application:
    result = await db.execute(
        select(Application).where(
            Application.id == application_id,
            Application.user_id == user_id,
        )
    )
    app = result.scalar_one_or_none()
    if app is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Application not found"
        )
    return app


async def create_application(
    db: AsyncSession, user_id: int, data: ApplicationCreate
) -> Application:
    app = Application(
        user_id=user_id,
        jd_source=data.jd_source,
        jd_type=data.jd_type,
        jd_text=data.jd_text,
        jd_url=data.jd_url,
    )
    db.add(app)
    await db.commit()
    await db.refresh(app)

    if data.run_analysis:
        app = await _run_and_persist_analysis(db, user_id, app)

    return app


async def update_application(
    db: AsyncSession, user_id: int, application_id: int, data: ApplicationUpdate
) -> Application:
    app = await get_application(db, user_id, application_id)
    if data.status is not None:
        app.status = data.status
    if data.cover_letter is not None:
        app.cover_letter = data.cover_letter
    if data.jd_url is not None:
        app.jd_url = data.jd_url
    app.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(app)
    return app


async def delete_application(
    db: AsyncSession, user_id: int, application_id: int
) -> None:
    app = await get_application(db, user_id, application_id)
    await db.delete(app)
    await db.commit()


async def list_comments(
    db: AsyncSession, user_id: int, application_id: int
) -> List[ApplicationComment]:
    await get_application(db, user_id, application_id)
    result = await db.execute(
        select(ApplicationComment)
        .where(ApplicationComment.application_id == application_id)
        .order_by(ApplicationComment.created_at.asc())
    )
    return list(result.scalars().all())


async def create_comment(
    db: AsyncSession, user_id: int, application_id: int, data: CommentCreate
) -> ApplicationComment:
    await get_application(db, user_id, application_id)
    comment = ApplicationComment(
        application_id=application_id,
        user_id=user_id,
        type=data.type,
        question=data.question,
        comment=data.comment,
    )
    db.add(comment)
    await db.commit()
    await db.refresh(comment)
    return comment


async def delete_comment(
    db: AsyncSession, user_id: int, application_id: int, comment_id: int
) -> None:
    await get_application(db, user_id, application_id)
    result = await db.execute(
        select(ApplicationComment).where(
            ApplicationComment.id == comment_id,
            ApplicationComment.application_id == application_id,
            ApplicationComment.user_id == user_id,
        )
    )
    comment = result.scalar_one_or_none()
    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found"
        )
    await db.delete(comment)
    await db.commit()


async def analyze_application(
    db: AsyncSession, user_id: int, application_id: int
) -> Application:
    app = await get_application(db, user_id, application_id)
    return await _run_and_persist_analysis(db, user_id, app)


async def stream_and_persist_analysis(
    db: AsyncSession, user_id: int, application_id: int
) -> AsyncGenerator[dict, None]:
    user_result = await db.execute(select(User).where(User.id == user_id))
    user = user_result.scalar_one_or_none()
    if not user or not user.is_email_verified:
        yield {
            "type": "error",
            "message": "Please verify your email before running analyses.",
            "status_code": 403,
        }
        return

    app = await get_application(db, user_id, application_id)
    profile = await get_or_create_profile(db, user_id)
    if not profile.cv_text:
        yield {
            "type": "error",
            "message": "No CV found. Upload your CV first. in profile section.",
        }
        return

    await check_and_increment_daily_limit(user_id, db)

    jd_type = app.jd_type or ("url" if app.jd_source.startswith("http") else "text")

    async for event in stream_analysis(
        profile.cv_text, jd_type, app.jd_source, user_id
    ):
        if event["type"] == "_state":
            state = event["state"]
            match_result = parse_json_field(state, "match_result")
            app.match_score = match_result.get("overall_score")
            app.match_breakdown = match_result
            app.ats_tips = parse_json_field(state, "ats_tips")
            app.jd_data = parse_json_field(state, "jd_data")
            app.updated_at = datetime.utcnow()
            await db.commit()
            await db.refresh(app)
            yield {
                "type": "done",
                "application": ApplicationResponse.model_validate(app).model_dump(
                    mode="json"
                ),
            }
        else:
            yield event


async def _run_and_persist_analysis(
    db: AsyncSession, user_id: int, app: Application
) -> Application:
    async for event in stream_and_persist_analysis(db, user_id, app.id):
        if event["type"] == "done":
            break
        if event["type"] == "error":
            status_code = event.get("status_code", status.HTTP_422_UNPROCESSABLE_ENTITY)
            raise HTTPException(
                status_code=status_code,
                detail=event["message"],
            )
    return await get_application(db, user_id, app.id)
