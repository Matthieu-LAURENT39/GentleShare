from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class ProfileForm(FlaskForm):
    displayname = StringField("Nom", validators=[DataRequired()])
    about = StringField("A propos de moi")
