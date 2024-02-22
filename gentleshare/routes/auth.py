from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user
from . import main
from ..database import User, db
from sqlalchemy.exc import IntegrityError


@main.route("/login", methods=["GET", "POST"])
def login() -> str:
    """Login route

    Returns:
        str: The login page
    """
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("main.index"))

        flash("Invalid username or password", "danger")

    return render_template("login.jinja")


@main.route("/register", methods=["GET", "POST"])
def register() -> str:
    """Register route

    Returns:
        str: The register page
    """
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        print(username, password)

        user = User(username=username)
        user.set_password(password)

        try:
            db.session.add(user)
            db.session.commit()
        # If the user already exists
        except IntegrityError:
            flash(f"Username is already taken", "danger")
            return render_template("register.jinja")

        flash("User created", "success")

    return render_template("register.jinja")
