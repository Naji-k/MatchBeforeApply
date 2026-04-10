import enum
from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Text,
    ForeignKey,
    Enum as SAEnum,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from db.database import Base


class ApplicationStatus(str, enum.Enum):
    open = "open"
    in_progress = "in_progress"
    rejected = "rejected"
    accepted = "accepted"


class CommentType(str, enum.Enum):
    general = "general"
    company = "company"
    interview = "interview"
    qa = "qa"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=True)
    full_name = Column(String(255), nullable=True)
    google_id = Column(String(255), unique=True, nullable=True, index=True)
    auth_provider = Column(String(50), nullable=False, server_default="local")
    created_at = Column(DateTime, default=datetime.utcnow)

    profile = relationship("UserProfile", back_populates="user", uselist=False)
    applications = relationship("Application", back_populates="user")
    comments = relationship("ApplicationComment", back_populates="user")


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id"), unique=True, nullable=False, index=True
    )
    cv_text = Column(Text, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="profile")


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    jd_source = Column(Text, nullable=False)
    jd_type = Column(String(10), nullable=True)
    jd_text = Column(Text, nullable=True)
    match_score = Column(Integer, nullable=True)
    match_breakdown = Column(JSONB, nullable=True)
    ats_tips = Column(JSONB, nullable=True)
    jd_data = Column(JSONB, nullable=True)
    cover_letter = Column(Text, nullable=True)
    status = Column(
        SAEnum(ApplicationStatus, name="applicationstatus"),
        default=ApplicationStatus.open,
        nullable=False,
    )
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="applications")
    comments = relationship(
        "ApplicationComment", back_populates="application", cascade="all, delete-orphan"
    )


class ApplicationComment(Base):
    __tablename__ = "application_comments"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(
        Integer, ForeignKey("applications.id"), nullable=False, index=True
    )
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    type = Column(
        SAEnum(CommentType, name="commenttype"),
        nullable=False,
        default=CommentType.general,
    )
    question = Column(Text, nullable=True)
    comment = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    application = relationship("Application", back_populates="comments")
    user = relationship("User", back_populates="comments")
