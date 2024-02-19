from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Expose the various models
from .user import User
