from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo


class RegisterForm(FlaskForm):
    username = StringField("Nom d'utilisateur", validators=[DataRequired()])
    password = PasswordField("Mot de passe", validators=[DataRequired()])
    password_confirm = PasswordField("Confirmation du mot de passe", validators=[DataRequired(), EqualTo("password", "Passwords must match")])
