from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired


class ProfileForm(FlaskForm):
    display_name = StringField("Nom", validators=[DataRequired()])
    display_first_name = StringField("Prénom", validators=[DataRequired()])
    display_email = StringField("email", validators=[DataRequired()])  
    about_me = TextAreaField("A propos de moi")
