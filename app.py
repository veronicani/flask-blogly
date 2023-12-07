"""Blogly application."""

import os

from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import User, db, connect_db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///flask_blogly')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secret"


connect_db(app)

debug = DebugToolbarExtension(app)
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


@app.get("/")
def show_homepage():
    return redirect("/users/")


@app.get("/users/")
def show_users():
    """Show all users and have links to user profiles and a link to the
        add-user form.

        Returns:
            users.html template
            users (list): all user objects from database
    """

    users = User.query.all()
    return render_template("users.html", users=users)
