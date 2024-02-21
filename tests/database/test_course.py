import pytest
from gentleshare import db
from gentleshare.database import User, Course
from gentleshare.classes import EducationLevel, Subject
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy.exc


def test_insert_course(app: Flask):
    # Create a user
    user = User(username="test_user")
    user.set_password("test_password")
    db.session.add(user)
    db.session.commit()

    # Create a course
    course = Course(
        owner=user,
        title="My cool course",
        description="I love teaching",
        education_level=EducationLevel.HIGH,
        subject=Subject.MATHS,
    )
    db.session.add(course)
    db.session.commit()

    # Retrieve the course from the database
    retrieved_course: Course = Course.query.filter_by(title="My cool course").first()
    assert retrieved_course is not None

    # Assert that the course fields are correctly set
    assert retrieved_course.title == "My cool course"
    assert retrieved_course.description == "I love teaching"
    assert retrieved_course.owner == user
    assert retrieved_course.education_level == EducationLevel.HIGH
    assert retrieved_course.subject == Subject.MATHS

    assert retrieved_course.reviews == []
    assert course in user.owned_courses
