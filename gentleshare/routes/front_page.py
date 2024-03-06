from flask import render_template
from flask_login import current_user

from ..database import File, User, Course
from . import main
from ..forms import ProfileForm
from ..database import db


@main.route("/")
def index():
    file_list: list[File] = File.query.order_by(File.uploaded_at.desc()).all()
    course_list: list[Course] = Course.query.order_by(Course.id.desc()).all()
    return render_template("index.jinja", file_list=file_list, course_list=course_list)


@main.route("/profile", methods=["GET", "POST"])
def profile():

    form = ProfileForm()

    if form.validate_on_submit():
        displayname = form.display_name.data
        about = form.about.data

        current_user: User = current_user
        current_user.display_name = displayname
        current_user.about_me = about

        db.session.add(current_user)
        db.session.commit()

    return render_template("profile.jinja", form=form)
