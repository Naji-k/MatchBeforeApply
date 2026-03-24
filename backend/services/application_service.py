from datetime import datetime
from typing import List

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Application, ApplicationComment
from schemas.application import ApplicationCreate, ApplicationUpdate, CommentCreate
from services.analyze_service import run_analysis
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


async def _run_and_persist_analysis(
    db: AsyncSession, user_id: int, app: Application
) -> Application:
    profile = await get_or_create_profile(db, user_id)
    if not profile.cv_text:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="No CV text found in profile. Update your profile with CV text before running analysis.",
        )

    jd_type = app.jd_type or ("url" if app.jd_source.startswith("http") else "text")
    result = await run_analysis(
        cv_text=profile.cv_text, jd_type=jd_type, jd_input=app.jd_source
    )

    match_result = result.get("match_result", {})
    app.match_score = match_result.get("overall_score")
    app.match_breakdown = match_result
    app.ats_tips = result.get("ats_tips", {})
    app.jd_data = result.get("jd_data", {})
    app.updated_at = datetime.utcnow()

    await db.commit()
    await db.refresh(app)
    return app
