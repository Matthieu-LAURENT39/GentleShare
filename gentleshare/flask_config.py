import secrets

from loguru import logger

_SECRET_KEY_FILE = "./secret_key.txt"


class Config:
    def __init__(self) -> None:
        try:
            with open(_SECRET_KEY_FILE, "r") as f:
                self.secret_key = f.read().strip()
        except FileNotFoundError:
            logger.warning(
                f"Secret key file not found at {_SECRET_KEY_FILE}. Generating new secret key."
            )
            self.secret_key = secrets.token_urlsafe(64)
            with open(_SECRET_KEY_FILE, "w") as f:
                f.write(self.secret_key)

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite"


class TestConfig(Config):
    def __init__(self) -> None: ...

    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SECRET_KEY = "test"
