from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField("Nom d'utilisateur", validators=[DataRequired()])
    password = StringField("Mot de passe", validators=[DataRequired()])
