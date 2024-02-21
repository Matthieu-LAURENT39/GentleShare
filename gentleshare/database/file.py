from __future__ import annotations

from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_file import FileField
from typing import TYPE_CHECKING
from .user_file_favorite import user_file_favorites

if TYPE_CHECKING:
    from .user import User

from . import db
from ..classes import EducationLevel, Subject

# import customidenticon


class File(db.Model):
    """A file uploaded by a user"""

    __tablename__ = "files"

    id: Mapped[int] = mapped_column(primary_key=True)

    owner_id = mapped_column(Integer, db.ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="uploaded_files")
    """The user who uploaded the file"""

    title: Mapped[str]
    """The title of the file"""
    description: Mapped[str]
    """The description of the file. Can contain Markdown."""

    education_level: Mapped[EducationLevel]
    """The education level the file is associated with"""
    subject: Mapped[Subject]
    """The subject the file is associated with"""

    content = mapped_column(FileField, nullable=False)
    """The actual file"""

    favorited_by: Mapped[list["User"]] = relationship(
        secondary=user_file_favorites, back_populates="favorited_files"
    )
    """The users who favorited the file"""
