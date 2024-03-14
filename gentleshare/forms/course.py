from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, TextAreaField
from wtforms.validators import DataRequired

from ..classes import EducationLevel, Subject


class AddCourseForm(FlaskForm):
    title = StringField("Titre", validators=[DataRequired()])
    """The title of the course"""
    description = TextAreaField("Description", validators=[DataRequired()])
    """The description of the course. Can contain Markdown."""

    education_level = SelectField(
        "Niveau d'éducation",
        choices=[(level.name, level.display_name) for level in EducationLevel],
    )
    """The education level the course is associated with"""
    subject = SelectField(
        "Matière", choices=[(subject.name, subject.display_name) for subject in Subject]
    )
    """The subject the course is associated with"""
