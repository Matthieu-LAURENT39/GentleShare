from flask import render_template, request, redirect, url_for, flash, session
from markupsafe import escape
from flask_login import login_user, current_user, logout_user
from . import main
from ..database import User, db, File
from sqlalchemy.exc import IntegrityError
from loguru import logger
from ..forms import LoginForm, RegisterForm

@main.route("/myfiles", methods=["GET", "POST"])
def myfiles() -> str:
    file_list: list[File] = File.query.order_by(File.uploaded_at.desc()).all()

    return render_template("my_file.jinja", file_list=file_list)