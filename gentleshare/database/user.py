"""
SQLAlchemy model for a user
"""

from __future__ import annotations

from flask_login import UserMixin
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import check_password_hash, generate_password_hash

from . import db

# import customidenticon


# We inherit from UserMixin to get the required @property for free
class User(db.Model, UserMixin):
    """A user of the website"""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    # collation="NOCASE" means the comparison is case-insensitive
    username: Mapped[str] = mapped_column(String(collation="NOCASE"), unique=True)
    # email: Mapped[str] = mapped_column(String(collation="NOCASE"), unique=True)
    password_hash: Mapped[str]
    """
    The password's hash, of the form 'method$salt$hash'
    See also: https://werkzeug.palletsprojects.com/en/1.0.x/utils/#werkzeug.security.generate_password_hash
    """

    def set_password(self, password: str) -> None:
        """Set the user's password by storing its hash

        Args:
            password (str): The new cleartext password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password: str) -> bool:
        """Checks if the given password is correct

        Args:
            password (str): The password in cleartext to check

        Returns:
            bool: True if the password is correct, False otherwise
        """
        return check_password_hash(self.password_hash, password)
