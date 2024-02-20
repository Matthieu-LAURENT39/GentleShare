from flask import render_template

from . import main


@main.route("/")
def main_page():
    return render_template("acceuil.jinja")
