from flask import render_template, request, redirect, url_for, flash, session
from markupsafe import escape
from flask_login import login_user, current_user, logout_user
from . import main
from ..database import User, db
from sqlalchemy.exc import IntegrityError
from loguru import logger
from ..forms import LoginForm, RegisterForm


@main.route("/login", methods=["GET", "POST"])
def login() -> str:
    """Login route"""
    if current_user.is_authenticated:
        flash("You are already logged in", "warning")
        return redirect(url_for("main.index"))

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user: User = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            if user.totp_enabled:
                logger.info(f"Sending '{username}' to TOTP validation")
                session["awaiting_totp"] = user.username
                return render_template("totp.jinja")

            logger.info(f"Logging in user '{username}'")
            login_user(user)
            return redirect(url_for("main.index"))

        logger.info(f"Failed login attempt for user '{username}'")
        flash("Invalid username or password", "danger")

    return render_template("login.jinja", form=form)


@main.route("/register", methods=["GET", "POST"])
def register() -> str:
    """Register route"""
    if current_user.is_authenticated:
        flash("You are already logged in", "warning")
        return redirect(url_for("main.index"))

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        logger.info(f"Registering user '{username}'")

        user = User(username=username)
        user.set_password(password)

        try:
            db.session.add(user)
            db.session.commit()
        # If the user already exists
        except IntegrityError:
            db.session.rollback()
            flash(f"Username '{escape(username)}' is already taken", "danger")
            return render_template("register.jinja")

        login_user(user)
        flash("User created", "success")

    return render_template("register.jinja")


@main.route("/logout")
def logout() -> str:
    """Logout route"""
    if current_user.is_authenticated:
        logout_user()
        flash("You have been logged out", "success")
    else:
        flash("You can't log out without being logged in", "warning")
    return redirect(url_for("main.index"))


@main.route("/totp", methods=["GET", "POST"])
def validate_totp() -> str:
    # This can't be forged, it's signed by the server
    username = session.get("awaiting_totp")
    if not username:
        return redirect(url_for("main.login"))

    if request.method == "POST":
        totp = request.form.get("totp")
        user: User = User.query.filter_by(username=username).first()

        if user.check_totp(totp):
            logger.info(f"Logging in user '{username}', after TOTP validation")
            login_user(user)
            session.pop("awaiting_totp")
            return redirect(url_for("main.index"))

        flash("Invalid TOTP code", "danger")

    return render_template("totp.jinja")
