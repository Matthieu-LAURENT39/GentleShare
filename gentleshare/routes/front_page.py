from flask import flash, render_template
from flask_login import current_user, login_required

from ..classes import FlashCategory
from ..database import Course, File, User, db
from ..forms import ProfileForm
from . import main


@main.route("/")
def index():
    """Route to the index page of the app"""
    file_list: list[File] = File.query.order_by(File.uploaded_at.desc()).all()
    course_list: list[Course] = Course.query.order_by(Course.id.desc()).all()
    return render_template("index.jinja", file_list=file_list, course_list=course_list)
