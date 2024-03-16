from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, TextAreaField
from wtforms.validators import DataRequired, Length


class AddCommentForm(FlaskForm):
    review = StringField(
        "Laisser un commentaire",
        validators=[
            DataRequired(),
            Length(
                min=3,
                max=300,
                message="Le commentaire doit faire entre %(min)d et %(max)d caractères",
            ),
        ],
    )
    rating = SelectField(
        "Note",
        choices=[(str(i), str(i)) for i in range(1, 11)]
    )
