from flask import render_template

from ..database import File
from . import main


@main.route("/")
def index():
    return render_template("acceuil.jinja")
@main.route("/profile_page")
def profile_page():
    return render_template("private_profile.jinja")
