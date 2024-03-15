from flask import flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required, login_user, logout_user
from loguru import logger
from markupsafe import escape
from sqlalchemy.exc import IntegrityError

from ..database import Course, File, User, db
from ..forms import LoginForm, RegisterForm
from . import main


@main.route("/files", methods=["GET", "POST"])
def list_files() -> str:
    file_list: list[File] = File.query.order_by(File.uploaded_at.desc()).all()

    return render_template("my_file.jinja", file_list=file_list)


@main.route("/courses", methods=["GET", "POST"])
def list_courses() -> str:
    course_list: list[Course] = Course.query.order_by(Course.id.desc()).all()

    return render_template("my_courses.jinja", course_list=course_list)


@main.route("/addtofav", methods=["GET", "POST"])
@login_required  # Assurez-vous que l'utilisateur est connecté
def addtofav() -> str:
    file_id = request.args.get(
        "file_id"
    )  # Obtenez l'ID du fichier à partir des paramètres de requête

    if file_id:
        file = File.query.get(file_id)
        if file:
            try:
                # Vérifiez d'abord si le fichier est déjà dans la liste des favoris
                if file not in current_user.favorited_files:
                    current_user.favorited_files.append(file)
                    db.session.commit()
                    flash("Fichier ajouté aux favoris avec succès.", "success")
                else:
                    flash("Ce fichier est déjà dans vos favoris.", "info")
            except IntegrityError:
                db.session.rollback()
                flash(
                    "Une erreur s'est produite lors de l'ajout du fichier aux favoris.",
                    "error",
                )
        else:
            flash("Fichier non trouvé.", "error")

    # Redirection ou affichage de la page, selon votre logique d'application
    return redirect(
        url_for("main.list_files")
    )  # Redirigez vers la liste de fichiers après l'ajout aux favoris
