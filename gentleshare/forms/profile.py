from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, EmailField, BooleanField
from wtforms.validators import DataRequired, Length
from wtforms.validators import Optional


class ProfileForm(FlaskForm):
    display_name = StringField(
        "Nom",
        validators=[
            Length(max=50, message="Le nom doit faire moins de %(max)d caractères")
        ],
    )
    email = EmailField(
        "Email",
        validators=[
            Length(max=250, message="L'email doit faire moins de %(max)d caractères")
        ],
    )
    phone_number = StringField(
        "Numéro de téléphone",
        validators=[
            Length(
                max=20,
                message="Le numéro de téléphone doit faire moins de %(max)d caractères",
            )
        ],
    )
    about_me = TextAreaField(
        "A propos de moi",
        validators=[
            Length(
                max=2500,
                message="La description doit faire moins de %(max)d caractères",
            )
        ],
    )
    totp_enabled = BooleanField(
    "Activation de totp",
    validators=[Optional()]
    )
