from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired


class ProfileForm(FlaskForm):
    display_name = StringField("Nom", validators=[DataRequired()])
    about = TextAreaField("A propos de moi")
