"""
Flask blueprints and routes
"""

from flask import Blueprint

main = Blueprint("main", __name__)

# flake8: noqa: E402
from . import front_page
from . import auth
