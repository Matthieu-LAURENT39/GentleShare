"""
Join table for users and their favorited files.
"""

from __future__ import annotations

from sqlalchemy import Table, Column

from . import db

user_file_favorites = Table(
    "user_file_favorites",
    db.metadata,
    Column("user_id", db.ForeignKey("users.id"), primary_key=True),
    Column("file_id", db.ForeignKey("files.id"), primary_key=True),
)
