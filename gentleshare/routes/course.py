from flask import render_template, flash, redirect, url_for

from ..database import Course
from ..classes import FlashCategory
from . import main


@main.route("/courses", methods=["GET", "POST"])
def list_courses() -> str:
    course_list: list[Course] = Course.query.order_by(Course.id.desc()).all()

    return render_template("my_courses.jinja", course_list=course_list)


@main.route("/courses/<int:course_id>")
def course(course_id: int) -> str:
    course_element = Course.query.get(course_id)
    if course_element is None:
        flash("Ce cours n'existe pas", FlashCategory.ERROR)
        return redirect(url_for("main.index"))

    return render_template("course.jinja", course=course_element)
