from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class ProfileForm(FlaskForm):
    display_name = StringField("Nom", validators=[DataRequired()])
    about = StringField("A propos de moi")
