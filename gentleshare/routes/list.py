from flask import render_template
from . import main
from ..database import File


@main.route("/list", methods=["GET", "POST"])
def list_files_classes() -> str:
    file_list: list[File] = File.query.all()
    return render_template("list.jinja", file_list=file_list)
