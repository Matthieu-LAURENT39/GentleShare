from flask import render_template, redirect, url_for, flash
import werkzeug.exceptions
from ..classes import FlashCategory

from . import main


@main.errorhandler(401)
def page_not_found(e: werkzeug.exceptions.Unauthorized):
    """Error handler for 401 Unauthorized"""

    flash("Vous devez être connecté pour accéder à cette page", FlashCategory.INFO)
    return redirect(url_for("main.login"))
