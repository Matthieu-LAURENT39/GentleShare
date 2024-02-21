from __future__ import annotations

from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import db
from ..classes import EducationLevel, Subject


class Course(db.Model):
    """A course advertised by a user, that can be reviewed by other users"""

    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True)

    owner_id = mapped_column(Integer, db.ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="owned_courses")
    """The user who offers the course"""

    title: Mapped[str]
    """The title of the course"""
    description: Mapped[str]
    """The description of the course. Can contain Markdown."""

    education_level: Mapped[EducationLevel]
    """The education level the course is associated with"""
    subject: Mapped[Subject]
    """The subject the course is associated with"""

    reviews = relationship("Review", back_populates="course")
    """The reviews left by users for this course"""
