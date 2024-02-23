from flask import render_template, request, redirect, url_for, flash
from markupsafe import escape
from flask_login import login_user
from . import main
from ..database import User, db, File
import sqlalchemy_file
from sqlalchemy.exc import IntegrityError
from flask_login import login_required, current_user
from ..classes import EducationLevel, Subject


@main.route("/upload", methods=["GET", "POST"])
@login_required
def upload_file() -> str:
    if request.method == "POST":
        uploaded_file = request.files["file"]
        f = File(
            owner=current_user,
            file_info=sqlalchemy_file.File(
                content=uploaded_file.stream, filename=uploaded_file.filename
            ),
            title="test",
            description="test",
            education_level=EducationLevel.HIGH,
            subject=Subject.MATHS,
        )
        db.session.add(f)
        db.session.commit()

    return render_template("upload.jinja")
