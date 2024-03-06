import sqlalchemy_file
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from loguru import logger

from ..classes import EducationLevel, Subject
from ..database import Course, File, db
from . import main


@main.route("/upload", methods=["GET", "POST"])
@login_required
def upload_file() -> str:
    if request.method == "POST":
        uploaded_file = request.files["file"]
        f = File(
            uploader=current_user,
            file_info=sqlalchemy_file.File(
                content=uploaded_file.stream, filename=uploaded_file.filename
            ),
            # TODO: Mettre des vrai valeurs
            title="test",
            description=request.form.get("description"),
            education_level=EducationLevel.HIGH,
            subject=Subject.MATHS,
        )
        db.session.add(f)
        db.session.commit()
        logger.info(
            f"User {current_user.username} uploaded file '{f.title}' ({f.file_info['file_id']})"
        )
        flash("Fichier téléversé!", "success")
        return redirect(url_for("main.index"))

    return render_template("file_upload.jinja")


@main.route("/create_course", methods=["GET", "POST"])
@login_required
def create_course() -> str:
    # if request.method == "POST":
    c = Course(
        owner=current_user,
        title="title",
        description="description",
        education_level=EducationLevel.MIDDLE,
        subject=Subject.ENGLISH,
    )

    db.session.add(c)
    db.session.commit()

    logger.info(f"User {current_user.username} created course '{c.title}' ({c.id})")
    flash("Cours créé!", "success")
    return redirect(url_for("main.index"))

    return render_template("course_create.jinja")
