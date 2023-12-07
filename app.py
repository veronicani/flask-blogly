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


@app.get("/users/new")
def show_new_user_form():
    """ Shows the new user form. 

        Fieldsets:
            First Name: "Enter a first name"
            Last Name: "Enter a last name"
            Image URL: "Provide an image of this user"

        Returns:
            new_user_form.html template
    """

    return render_template("new_user_form.html")


@app.get("/users/<int:user_id>")
def show_user_detail_page(user_id):
    """ Shows the page of information of a given user.
        Contains options to edit or delete user profile.

        Returns:
            user_details.html template
            user object with the corresponding id
    """

    user = User.query.get_or_404(user_id)
    return render_template("user_details.html", user=user)
