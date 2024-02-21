import pytest
from gentleshare import db
from gentleshare.database import User, Course, Review
from gentleshare.classes import EducationLevel, Subject
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy.exc


def test_insert_review(app: Flask):
    """Test that a valid review can be inserted into the database"""
    user = User(username="test_user")
    user.set_password("test_password")
    db.session.add(user)
    course = Course(
        owner=user,
        title="My cool course",
        description="I love teaching",
        education_level=EducationLevel.HIGH,
        subject=Subject.MATHS,
    )
    db.session.add(course)
    db.session.commit()

    # Create a review
    review = Review(
        course=course,
        reviewer=user,
        rating=9,
        comment="Great course!",
    )
    db.session.add(review)
    db.session.commit()

    # Retrieve the review from the database
    retrieved_review: Review = Review.query.filter_by(course=course, rating=9).first()
    assert retrieved_review is not None

    # Assert that the review fields are correctly set
    assert retrieved_review.course == course
    assert retrieved_review.reviewer == user
    assert retrieved_review.rating == 9
    assert retrieved_review.comment == "Great course!"

    assert review in course.reviews
    assert review in user.reviews


@pytest.mark.parametrize("rating", [-1, 11])
def test_review_invalid_rating(app: Flask, rating: int):
    """Test that a review with an invalid rating cannot be inserted into the database"""
    user = User(username="test_user")
    user.set_password("test_password")
    db.session.add(user)
    course = Course(
        owner=user,
        title="My cool course",
        description="I love teaching",
        education_level=EducationLevel.HIGH,
        subject=Subject.MATHS,
    )
    db.session.add(course)
    db.session.commit()

    # Create a review with invalid rating
    with pytest.raises(ValueError):
        review = Review(
            course=course,
            reviewer=user,
            rating=rating,
            comment="Great course!",
        )
        db.session.add(review)
        db.session.commit()
