import pytest
from gentleshare import create_app
from gentleshare.flask_config import TestConfig


@pytest.fixture()
def app():
    app = create_app(config=TestConfig)

    # other setup can go here

    with app.app_context():
        yield app

    # clean up / reset resources here
