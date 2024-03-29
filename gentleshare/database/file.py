from __future__ import annotations

from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from flask import url_for
import sqlalchemy_file
from typing import TYPE_CHECKING
from sqlalchemy_file.storage import StorageManager
from .user_file_favorite import user_file_favorites
from datetime import datetime, UTC
import humanize

if TYPE_CHECKING:
    from .user import User

from . import db
from ..classes import EducationLevel, Subject


class File(db.Model):
    """A file uploaded by a user"""

    __tablename__ = "files"

    def __init__(self, *args, **kwargs):
        # sqlalchemy_file.FileField doesn't support nullable=False, we
        # have to do the check ourselves
        if kwargs.get("file_info") is None:
            # We can't raise IntegrityError ourselves, so we use ValueError
            raise ValueError("file_info cannot be None")
        super().__init__(*args, **kwargs)

    id: Mapped[int] = mapped_column(primary_key=True)
    """The id of the file"""

    uploaded_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))
    """The date and time the file was uploaded, in UTC"""

    uploader_id = mapped_column(Integer, db.ForeignKey("users.id"), nullable=False)
    uploader = relationship("User", back_populates="uploaded_files")
    """The user who uploaded the file"""

    title: Mapped[str]
    """The title of the file"""
    description: Mapped[str]
    """The description of the file. Can contain Markdown."""

    education_level: Mapped[EducationLevel]
    """The education level the file is associated with"""
    subject: Mapped[Subject]
    """The subject the file is associated with"""

    # file_info: Mapped[sqlalchemy_file.StoredFile] = mapped_column(
    #     sqlalchemy_file.FileField(upload_storage="files"), nullable=False
    # )
    file_info = mapped_column(
        sqlalchemy_file.FileField(upload_storage="files"), nullable=False
    )
    """The info about the actual file"""

    favorited_by: Mapped[list["User"]] = relationship(
        secondary=user_file_favorites, back_populates="favorited_files"
    )
    """The users who favorited the file"""

    @property
    def stored_file(self):
        """The actual file stored in the storage backend"""
        return StorageManager.get_file(self.file_info["path"])

    @property
    def file_url(self):
        """The URL to the file"""
        return url_for(
            "main.serve_files",
            storage=self.file_info["upload_storage"],
            file_id=self.file_info["file_id"],
        )

    @property
    def file_size(self) -> int:
        """File size, in bytes"""
        return self.file_info["size"]

    @property
    def pretty_file_size(self) -> str:
        """File size, in a human-readable format"""
        return humanize.naturalsize(self.file_size)
