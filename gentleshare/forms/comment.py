from flask_wtf import FlaskForm
from wtforms import SelectField, TextAreaField
from wtforms.validators import DataRequired, Length


class AddCommentForm(FlaskForm):
    review = TextAreaField(
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
    rating = SelectField("Note", choices=[(str(i), str(i)) for i in range(1, 11)])

    def validate_rating(self, field):
        try:
            rating = int(field.data)
        except ValueError:
            raise ValueError("La note doit être un nombre entier.")

        if not (1 <= rating <= 10):
            raise ValueError("La note doit être entre 1 et 10, inclusivement.")
