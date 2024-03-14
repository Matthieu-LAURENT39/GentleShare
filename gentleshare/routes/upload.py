import sqlalchemy_file
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from loguru import logger

from ..classes import EducationLevel, Subject, FlashCategory
from ..database import Course, File, db
from ..forms import AddCourseForm, AddFileForm
from . import main


@main.route("/upload", methods=["GET", "POST"])
@login_required
def upload_file() -> str:
    form = AddFileForm()

    if form.validate_on_submit():
        # Users can have a max of 250 files
        if len(current_user.uploaded_files) >= 250:
            flash("Vous avez atteint la limite de 250 fichiers", FlashCategory.ERROR)
            return redirect(url_for("main.index"))

        f = File(
            uploader=current_user,
            file_info=sqlalchemy_file.File(
                content=form.file.data.stream, filename=form.file.data.filename
            ),
            title=form.title.data,
            description=form.description.data,
            education_level=EducationLevel[form.education_level.data],
            subject=Subject[form.subject.data],
        )

        db.session.add(f)
        db.session.commit()

        logger.info(
            f"User {current_user.username} uploaded file '{f.title}' ({f.file_info['file_id']})"
        )
        flash("Fichier téléversé!", FlashCategory.SUCCESS)
        return redirect(url_for("main.index"))

    return render_template("file_upload.jinja", form=form)


@main.route("/create_course", methods=["GET", "POST"])
@login_required
def create_course() -> str:
    form = AddCourseForm()

    if form.validate_on_submit():
        c = Course(
            owner=current_user,
            title=form.title.data,
            description=form.description.data,
            education_level=EducationLevel[form.education_level.data],
            subject=Subject[form.subject.data],
        )

        db.session.add(c)
        db.session.commit()

        logger.info(f"User {current_user.username} created course '{c.title}' ({c.id})")
        flash("Cours créé!", FlashCategory.SUCCESS)
        return redirect(url_for("main.index"))

    return render_template("create_course.jinja", form=form)
