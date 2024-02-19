from __future__ import annotations

import contextlib
import glob
from typing import TYPE_CHECKING, Optional

from flask import Flask
from flask_login import LoginManager

from .flask_config import Config

from .database import db, User


login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id: str) -> Optional["User"]:
    """User loader for flask-login

    Args:
        user_id (str): The id of the user to load

    Returns:
        Optional[User]: The user if found, None otherwise
    """

    return User.query.filter_by(id=user_id).first()


def create_app(config: object = Config) -> Flask:
    """App factory for the Flask app

    Args:
        config (object, optional): The configuration to use. Defaults to Config.

    Returns:
        Flask: The flask app
    """
    app = Flask(
        __name__,
        static_folder="static",
        template_folder="templates",
        static_url_path="/static",
    )

    # We load the flask config
    app.config.from_object(config)

    # SQLalchemy
    db.init_app(app)

    # flask-login
    login_manager.init_app(app)

    with app.app_context():
        db.create_all()

    # Register the blueprints
    from .routes import main

    app.register_blueprint(main)

    # print(app.url_map)

    return app
