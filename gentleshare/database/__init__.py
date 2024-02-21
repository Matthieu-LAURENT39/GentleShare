from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Expose the various models
from .user import User
from .file import File
from .course import Course
from .review import Review
