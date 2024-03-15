from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField(
        "Nom d'utilisateur",
        validators=[
            DataRequired(),
            Length(
                min=5,
                max=25,
                message="Le nom d'utilisateur doit faire entre %(min)d et %(max)d caractères",
            ),
        ],
    )
    password = PasswordField("Mot de passe", validators=[DataRequired()])
