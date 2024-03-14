from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, FileField
from wtforms.validators import DataRequired
from flask_wtf.file import FileRequired

from ..classes import EducationLevel, Subject
from . import AddCourseForm


# For now it's almost the exact same as AddCourseForm, so we just recycle it
class AddFileForm(AddCourseForm):
    file = FileField(
        "Fichier",
        validators=[
            DataRequired(),
            FileRequired(),
        ],
    )
    """The file to upload"""
