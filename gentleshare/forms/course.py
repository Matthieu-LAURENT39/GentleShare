from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, TextAreaField
from wtforms.validators import DataRequired, Length

from ..classes import EducationLevel, Subject


class AddCourseForm(FlaskForm):
    """Form to add a course"""

    title = StringField(
        "Titre",
        validators=[
            DataRequired(),
            Length(
                min=3,
                max=100,
                message="Le titre doit faire entre %(min)d et %(max)d caractères",
            ),
        ],
    )
    """The title of the course"""
    description = TextAreaField(
        "Description",
        validators=[
            Length(
                max=500, message="La description doit faire moins de %(max)d caractères"
            )
        ],
    )
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
