from __future__ import annotations

from pprint import pprint
from typing import TYPE_CHECKING, Callable, Optional

from flask import Flask
from flask_login import LoginManager
from loguru import logger

from .database import User, db
from .flask_config import Config

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


def create_app(config: object | Callable = Config) -> Flask:
    """App factory for the Flask app

    Args:
        config (object, optional): The configuration to use. Defaults to Config.
            If the config is a callable, it will be called to get the config object.
            Classes are callables, so their init method will be called.

    Returns:
        Flask: The flask app
    """
    app = Flask(
        __name__,
        static_folder="static",
        template_folder="templates",
        static_url_path="/static",
    )

    # Calls init,
    if callable(config):
        config = config()

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

    if app.debug:
        print(" URL Map ".center(50, "="))
        for rule in app.url_map.iter_rules():
            print(f"{rule} ({rule.endpoint})")
        print("=" * 50)

    return app
