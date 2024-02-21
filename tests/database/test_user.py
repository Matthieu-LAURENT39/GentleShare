import pytest
from gentleshare import db
from gentleshare.database import User
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy.exc


def test_insert_user(app: Flask):
    # Create a new user
    user = User(username="test_user")
    user.set_password("test_password")

    db.session.add(user)
    db.session.commit()

    # Retrieve the user from the database
    retrieved_user = User.query.filter_by(username="test_user").first()
    assert retrieved_user is not None

    # Assert that the user fields are correctly set
    assert retrieved_user.username == "test_user"
    assert retrieved_user.about_me == None
    assert retrieved_user.totp_enabled == False


def test_user_no_password(app: Flask):
    user = User(username="test_user")

    with pytest.raises(sqlalchemy.exc.IntegrityError):
        # Add the user to the database without setting a password
        db.session.add(user)
        db.session.commit()


def test_password():
    user = User(username="test_user")

    # Set password for the user
    user.set_password("test_password")

    assert user.password_hash is not None

    assert user.check_password("test_password") == True
    assert user.check_password("wrong_password") == False

    assert user.password_hash != "test_password"
