from flask import render_template, request, redirect, url_for, flash, session
from markupsafe import escape
from flask_login import login_user, current_user, logout_user, login_required
from . import main
from ..database import User, db, File, Course
from sqlalchemy.exc import IntegrityError
from loguru import logger
from ..forms import LoginForm, RegisterForm

@main.route("/myfiles", methods=["GET", "POST"])
def myfiles() -> str:
    file_list: list[File] = File.query.order_by(File.uploaded_at.desc()).all()

    return render_template("my_file.jinja", file_list=file_list)

@main.route("/mycourses", methods=["GET", "POST"])
def mycourses() -> str:
    course_list: list[Course] = Course.query.order_by(Course.id.desc()).all()
    
    return render_template("my_courses.jinja", course_list=course_list)

@main.route("/addtofav", methods=["GET", "POST"])
@login_required  # Assurez-vous que l'utilisateur est connecté
def addtofav() -> str:
    file_id = request.args.get('file_id')  # Obtenez l'ID du fichier à partir des paramètres de requête

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
                flash("Une erreur s'est produite lors de l'ajout du fichier aux favoris.", "error")
        else:
            flash("Fichier non trouvé.", "error")

    # Redirection ou affichage de la page, selon votre logique d'application
    return redirect(url_for('main.myfiles'))  # Redirigez vers la liste de fichiers après l'ajout aux favoris