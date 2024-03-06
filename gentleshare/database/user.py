"""
SQLAlchemy model for a user
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

import pyotp
from flask_login import UserMixin
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import check_password_hash, generate_password_hash

from .user_file_favorite import user_file_favorites

if TYPE_CHECKING:
    from .file import File
    from .course import Course
    from .review import Review

from . import db

# import customidenticon


# We inherit from UserMixin to get the required @property for free
class User(db.Model, UserMixin):
    """A user of the website"""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    # collation="NOCASE" means the comparison is case-insensitive
    username: Mapped[str] = mapped_column(String(collation="NOCASE"), unique=True)
    about_me: Mapped[Optional[str]]
    # email: Mapped[str] = mapped_column(String(collation="NOCASE"), unique=True)
    password_hash: Mapped[str]
    """
    The password's hash, of the form 'method$salt$hash'
    See also:
    https://werkzeug.palletsprojects.com/en/1.0.x/utils/#werkzeug.security.generate_password_hash
    """

    # TODO: Add an actual totp token
    totp_secret: Mapped[str] = mapped_column(default="CHANGEME")
    """
    The secret for the TOTP (Time-based One-Time Password) algorithm
    """
    totp_enabled: Mapped[bool] = mapped_column(default=False)

    uploaded_files: Mapped[list["File"]] = relationship(
        "File", back_populates="uploader"
    )
    """The files uploaded by the user"""

    owned_courses: Mapped[list["Course"]] = relationship(
        "Course", back_populates="owner"
    )
    """The courses offered by the user"""

    favorited_files: Mapped[list["File"]] = relationship(
        secondary=user_file_favorites, back_populates="favorited_by"
    )
    """The files favorited by the user"""

    reviews: Mapped[list["Review"]] = relationship("Review", back_populates="reviewer")
    """The reviews left by the user"""

    def set_password(self, password: str) -> None:
        """Set the user's password by storing its hash

        Args:
            password (str): The new cleartext password
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Checks if the given password is correct

        Args:
            password (str): The password in cleartext to check

        Returns:
            bool: True if the password is correct, False otherwise
        """
        return check_password_hash(self.password_hash, password)

    @property
    def _totp(self) -> pyotp.TOTP:
        return pyotp.TOTP(self.totp_secret)

    def check_totp(self, code: int, valid_window: int = 3) -> bool:
        """Checks if the given TOTP token is correct

        Args:
            token (str): The TOTP token to check

        Returns:
            bool: True if the token is correct, False otherwise
        """
        return self._totp.verify(code, valid_window=valid_window)

    @property
    def totp_uri(self) -> str:
        """Generates a QR code for the TOTP secret

        Returns:
            str: The URL of the QR code
        """
        return self._totp.provisioning_uri(
            name=self.username, issuer_name="GentleShare"
        )
