from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    """Form for logging in a user"""

    username = StringField(
        "Nom d'utilisateur",
        validators=[DataRequired()],
    )
    password = PasswordField("Mot de passe", validators=[DataRequired()])
