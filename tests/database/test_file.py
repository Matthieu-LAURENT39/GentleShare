import pytest
from gentleshare import db
from gentleshare.database import User, File
from gentleshare.classes import EducationLevel, Subject
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy.exc


def test_insert_and_favorite_file(app: Flask):
    """Test that a valid file can be inserted into the database"""
    user = User(username="test_user")
    user.set_password("test_password")
    db.session.add(user)
    db.session.commit()

    # Create a file
    file = File(
        owner=user,
        title="My cool file",
        description="Epic file",
        education_level=EducationLevel.HIGH,
        subject=Subject.ENGLISH,
    )
    db.session.add(file)
    db.session.commit()

    # Retrieve the file from the database
    retrieved_file: File = File.query.filter_by(title="My cool file").first()
    assert retrieved_file is not None

    # Assert that the file fields are correctly set
    assert retrieved_file.title == "My cool file"
    assert retrieved_file.description == "Epic file"
    assert retrieved_file.owner == user
    assert retrieved_file.education_level == EducationLevel.HIGH
    assert retrieved_file.subject == Subject.ENGLISH

    assert retrieved_file.favorited_by == []
    assert file in user.uploaded_files

    # Test favoriting the file
    user.favorited_files.append(file)
    db.session.commit()

    assert file in user.favorited_files
    assert user in file.favorited_by
