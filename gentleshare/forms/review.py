from flask_wtf import FlaskForm
from wtforms import SelectField, TextAreaField
from wtforms.validators import DataRequired, Length


class AddReviewForm(FlaskForm):
    """Form to add a review to a course."""

    comment = TextAreaField(
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
    """The comment of the review. Can contain Markdown."""
    rating = SelectField(
        "Note", choices=[(str(i), str(i)) for i in range(1, 11)], coerce=int
    )
    """The rating of the course, from 1 to 10."""

    def validate_rating(self, field):
        """Validate the rating field."""

        try:
            rating = int(field.data)
        except ValueError:
            raise ValueError("La note doit être un nombre entier.")

        if not (1 <= rating <= 10):
            raise ValueError("La note doit être entre 1 et 10, inclusivement.")

        return rating
