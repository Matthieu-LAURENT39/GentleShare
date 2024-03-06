from . import main

from flask import render_template
from flask_login import login_required


@login_required
@main.route("/settings")
def settings():
    return render_template("settings.jinja")
