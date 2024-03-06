from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class InscriptionForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])