from flask import render_template

from ..database import File
from . import main


@main.route("/")
def index():
    file_list: list[File] = File.query.all()
    return render_template("index.jinja", file_list=file_list)
