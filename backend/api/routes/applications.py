from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.middleware import get_current_user
from db.database import get_db
from db.models import User
from schemas.application import (
    ApplicationCreate,
    ApplicationResponse,
    ApplicationUpdate,
    CommentCreate,
    CommentResponse,
)
from services.application_service import (
    analyze_application,
    create_application,
    create_comment,
    delete_application,
    delete_comment,
    get_application,
    list_applications,
    list_comments,
    update_application,
)

router = APIRouter(prefix="/api/applications", tags=["applications"])
"""
CRUD endpoints for managing job applications, plus comments and analysis trigger.
- `GET /api/applications`: List all applications for the current user.
- `POST /api/applications`: Create a new application with JD source/type; optionally run analysis immediately.
- `GET /api/applications/{id}`: Get details of a single application.
- `PATCH /api/applications/{id}`: Update application status or cover letter.
- `DELETE /api/applications/{id}`: Delete an application and its comments.
- `GET /api/applications/{id}/comments`: List comments for an application.
- `POST /api/applications/{id}/comments`: Add a comment to an application.
- `DELETE /api/applications/{id}/comments/{comment_id}`: Delete a specific comment.
- `POST /api/applications/{id}/analyze`: Trigger analysis for an existing"""

@router.get("", response_model=List[ApplicationResponse])
async def list_apps(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await list_applications(db, current_user.id)


@router.post(
    "", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED
)
async def create_app(
    data: ApplicationCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await create_application(db, current_user.id, data)


@router.get("/{application_id}", response_model=ApplicationResponse)
async def get_app(
    application_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await get_application(db, current_user.id, application_id)


@router.patch("/{application_id}", response_model=ApplicationResponse)
async def update_app(
    application_id: int,
    data: ApplicationUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await update_application(db, current_user.id, application_id, data)


@router.delete("/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_app(
    application_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await delete_application(db, current_user.id, application_id)


@router.get("/{application_id}/comments", response_model=List[CommentResponse])
async def get_comments(
    application_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await list_comments(db, current_user.id, application_id)


@router.post(
    "/{application_id}/comments",
    response_model=CommentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add_comment(
    application_id: int,
    data: CommentCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await create_comment(db, current_user.id, application_id, data)


@router.delete(
    "/{application_id}/comments/{comment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_comment(
    application_id: int,
    comment_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await delete_comment(db, current_user.id, application_id, comment_id)


@router.post("/{application_id}/analyze", response_model=ApplicationResponse)
async def trigger_analysis(
    application_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await analyze_application(db, current_user.id, application_id)
