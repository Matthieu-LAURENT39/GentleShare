from flask import render_template, redirect, url_for, flash
import werkzeug.exceptions

from . import main


@main.errorhandler(401)
def page_not_found(e: werkzeug.exceptions.Unauthorized):
    flash("Vous devez être connecté pour accéder à cette page", "info")
    return redirect(url_for("main.login"))
