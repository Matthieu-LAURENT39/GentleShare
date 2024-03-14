from flask import flash, render_template
from flask_login import current_user, login_required

from ..classes import FlashCategory
from ..database import Course, File, User, db
from ..forms import ProfileForm
from . import main


@main.route("/")
def index():
    file_list: list[File] = File.query.order_by(File.uploaded_at.desc()).all()
    course_list: list[Course] = Course.query.order_by(Course.id.desc()).all()
    return render_template("index.jinja", file_list=file_list, course_list=course_list)


@main.route("/settings", methods=["GET", "POST"])
@login_required
def settings():

    form = ProfileForm(obj=current_user)
    user: User = current_user

    if form.validate_on_submit():
        user.display_name = form.display_name.data
        user.about_me = form.about_me.data
        user.email = form.email.data
        user.phone_number = form.phone_number.data

        db.session.add(user)
        db.session.commit()
        flash("Profil mis à jour!", FlashCategory.SUCCESS)

    return render_template("settings.jinja", form=form)


@main.route("/profile/<username>")
def profile(username: str):
    user: User = User.query.filter_by(username=username).first()
    if user is None:
        flash("Cet utilisateur n'existe pas", FlashCategory.ERROR)
        return render_template("index.jinja")
    return render_template("profile.jinja", user=user)
