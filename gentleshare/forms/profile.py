from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, EmailField
from wtforms.validators import DataRequired, Length


class ProfileForm(FlaskForm):
    display_name = StringField("Nom", validators=[])
    email = EmailField("Email", validators=[])
    phone_number = StringField("Numéro de téléphone", validators=[])
    about_me = TextAreaField("A propos de moi", validators=[Length(max=2500)])
