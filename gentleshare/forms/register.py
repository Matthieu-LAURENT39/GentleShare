from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Length


class RegisterForm(FlaskForm):
    """Form for registering a new user"""

    username = StringField(
        "Nom d'utilisateur",
        validators=[
            DataRequired(),
            Length(
                min=4,
                max=25,
                message="Le nom d'utilisateur doit faire entre %(min)d et %(max)d caractères",
            ),
        ],
    )
    """The username of the user"""

    password = PasswordField(
        "Mot de passe",
        validators=[
            DataRequired(),
            Length(
                max=100,
                message="Le mot de passe doit faire entre %(min)d et %(max)d caractères",
            ),
        ],
    )
    """The password of the user"""

    password_confirm = PasswordField(
        "Confirmation du mot de passe",
        validators=[DataRequired(), EqualTo("password", "Passwords must match")],
    )
    """The password confirmation of the user"""
