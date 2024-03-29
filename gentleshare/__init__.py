from __future__ import annotations

from pprint import pprint
from typing import TYPE_CHECKING, Callable, Optional

import humanize.i18n
from flask import Flask
from flask_login import LoginManager
from flask_qrcode import QRcode
from libcloud.storage.drivers.local import LocalStorageDriver, StorageDriver
from loguru import logger

from . import filters
from .classes import setup_storage_manager
from .database import User, db
from .flask_config import Config

login_manager = LoginManager()
qrcode = QRcode()


@login_manager.user_loader
def load_user(user_id: str) -> Optional["User"]:
    """User loader for flask-login

    Args:
        user_id (str): The id of the user to load

    Returns:
        Optional[User]: The user if found, None otherwise
    """

    return User.query.filter_by(id=user_id).first()


# Setup the locale for humanize
humanize.i18n.activate("fr_FR")


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

    # Calls init
    if callable(config):
        config = config()

    # We load the flask config
    app.config.from_object(config)

    # Setup the storage manager
    setup_storage_manager(app, ignore_if_already_registered=app.config["TESTING"])

    # SQLalchemy
    db.init_app(app)

    # flask-login
    login_manager.init_app(app)

    # flask-qrcode
    qrcode.init_app(app)

    with app.app_context():
        db.create_all()

    # Register the filters
    app.jinja_env.filters["markdown"] = filters.markdown_filter

    # Register the blueprints
    from .routes import main

    app.register_blueprint(main)

    if app.debug:
        print(" URL Map ".center(50, "="))
        for rule in app.url_map.iter_rules():
            print(f"{rule} ({rule.endpoint})")
        print("=" * 50)

    return app
