"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


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
        db.CheckConstraint('len(name) >= 2'),
        nullable=False)
    last_name = db.Column(
        db.String(25),
        db.CheckConstraint('len(name) >= 2'),
        nullable=False)
    image_url = db.Column(
        db.Text,
        nullable=False,
        default="")
