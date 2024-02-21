"""
SQLAlchemy model for a review of a course by a user.
"""

from __future__ import annotations

from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy_file import FileField

from . import db
from ..classes import EducationLevel, Subject


class Review(db.Model):
    """A review of a course by a user"""

    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(primary_key=True)

    reviewer_id = mapped_column(Integer, db.ForeignKey("users.id"), nullable=False)
    reviewer = relationship("User", back_populates="reviews")
    """The user who reviewed the course"""

    course_id = mapped_column(Integer, db.ForeignKey("courses.id"), nullable=False)
    course = relationship("Course", back_populates="reviews")
    """The course that was reviewed"""

    rating: Mapped[int]
    """
    The rating the user gave to the course
    Goes from 0 to 10, with 0 being 0 stars and 10 being 5 stars
    (an odd number gives a half-star)
    """
    comment: Mapped[str]
    """
    The comment the user left for the course
    Can contain Markdown.
    """

    @validates("rating")
    def validate_rating(self, key, value: int):
        if not (0 <= value <= 10):
            raise ValueError("Rating must be between 0 and 10, inclusive.")
        return value
