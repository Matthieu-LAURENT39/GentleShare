from flask import flash, render_template
from flask_login import current_user, login_required

from ..classes import FlashCategory
from ..database import User, db
from ..forms import ProfileForm
from . import main


@main.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    """Route to manage the user settings"""

    form = ProfileForm(obj=current_user)
    user: User = current_user

    if form.validate_on_submit():
        user.display_name = form.display_name.data
        user.about_me = form.about_me.data
        user.email = form.email.data
        user.phone_number = form.phone_number.data
        user.totp_enabled = form.totp_enabled.data is True

        db.session.add(user)
        db.session.commit()
        flash("Profil mis à jour!", FlashCategory.SUCCESS)

    return render_template("settings.jinja", form=form)


@main.route("/profile/<username>")
def profile(username: str):
    """Route to view a user profile"""

    user: User = User.query.filter_by(username=username).first()
    if user is None:
        flash("Cet utilisateur n'existe pas", FlashCategory.ERROR)
        return render_template("index.jinja")
    return render_template("profile.jinja", user=user)
