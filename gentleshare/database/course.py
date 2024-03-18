from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..classes import EducationLevel, Subject
from . import db


class Course(db.Model):
    """A course advertised by a user, that can be reviewed by other users"""

    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True)
    """The id of the course"""

    owner_id = mapped_column(Integer, db.ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="owned_courses")
    """The user who offers the course"""

    title: Mapped[str]
    """The title of the course"""
    description: Mapped[str]
    """The description of the course. Can contain Markdown."""

    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))
    """The date and time the course was created, in UTC"""

    education_level: Mapped[EducationLevel]
    """The education level the course is associated with"""
    subject: Mapped[Subject]
    """The subject the course is associated with"""

    reviews = relationship("Review", back_populates="course")
    """The reviews left by users for this course"""
