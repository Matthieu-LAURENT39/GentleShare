from flask import render_template, request, redirect, url_for, flash
from markupsafe import escape
from flask_login import login_user
from . import main
from ..database import User, db, File
import sqlalchemy_file
from sqlalchemy.exc import IntegrityError
from flask_login import login_required, current_user
from ..classes import EducationLevel, Subject
from loguru import logger


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
            # TODO: Mettre des vrai valeurs
            title="test",
            description="test",
            education_level=EducationLevel.HIGH,
            subject=Subject.MATHS,
        )
        db.session.add(f)
        db.session.commit()
        logger.info(
            f"User {current_user.username} uploaded file '{f.title}' ({f.file_info['file_id']})"
        )
        flash("Fichier téléversé!", "success")
        return redirect(url_for("main.list_files_classes"))

    return render_template("upload.jinja")
