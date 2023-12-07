"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
print("MODELS.PY")


db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://tinyurl.com/mry92yn3"


def connect_db(app):
    """Connect to the database."""

    app.app_context().push()
    db.app = app
    db.init_app(app)


class User(db.Model):
    """
    User Class for Blogly.
    Fields:
        - id (Primary Key): Id of user. Auto-incrementing.
        - first_name: First name of user. Not NULL-able.
        - last_name: Last name of user. Not NULL-able.
        - image_url: A url to the profile image for user. Not NULL-able.
    """
    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)
    first_name = db.Column(
        db.String(25),
        nullable=False)
    last_name = db.Column(
        db.String(25),
        nullable=False)
    image_url = db.Column(
        db.Text,
        nullable=False,
        default=DEFAULT_IMAGE_URL)
