from flask import render_template
from flask_login import current_user

from ..database import File, User
from . import main
from ..forms import ProfileForm


@main.route("/")
def index():
    file_list: list[File] = File.query.all()
    return render_template("index.jinja", file_list=file_list)


@main.route("/profile", methods=["GET", "POST"])
def profile():

    form = ProfileForm()

    if form.validate_on_submit():
        displayname = form.displayname.data
        about = form.about.data
        
        current_user: User = current_user
        current_user.displayname = displayname

        


    return render_template("profile.jinja", form=form)
