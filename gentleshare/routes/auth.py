from flask import render_template, request, redirect, url_for, flash
from markupsafe import escape
from flask_login import login_user, current_user, logout_user
from . import main
from ..database import User, db
from sqlalchemy.exc import IntegrityError
from loguru import logger


@main.route("/login", methods=["GET", "POST"])
def login() -> str:
    """Login route"""
    if current_user.is_authenticated:
        flash("You are already logged in", "warning")
        return redirect(url_for("main.index"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        totp = request.form.get("totp")

        user: User = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            if user.totp_enabled:
                if not user.check_totp(totp):
                    logger.info(
                        f"Failed login attempt for user '{username}' (invalid TOTP code)"
                    )
                    flash("Invalid TOTP code", "danger")
                    return render_template("login.jinja")

            logger.info(f"Logging in user '{username}'")
            login_user(user)
            return redirect(url_for("main.index"))

        logger.info(f"Failed login attempt for user '{username}' (invalid credentials)")
        flash("Invalid username or password", "danger")

    return render_template("login.jinja")


@main.route("/register", methods=["GET", "POST"])
def register() -> str:
    """Register route"""
    if current_user.is_authenticated:
        flash("You are already logged in", "warning")
        return redirect(url_for("main.index"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

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
