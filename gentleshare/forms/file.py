from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, FileField
from wtforms.validators import DataRequired
from flask_wtf.file import FileRequired, FileSize

from ..classes import EducationLevel, Subject
from . import AddCourseForm


# For now it's almost the exact same as AddCourseForm, so we just recycle it
class AddFileForm(AddCourseForm):
    file = FileField(
        "Fichier",
        validators=[
            DataRequired(),
            FileRequired(),
            FileSize(
                max_size=10 * 1024 * 1024,
                message="Le fichier est trop gros. Taille max: 10 Mo",
            ),  # 10 Mo
        ],
    )
    """The file to upload"""
