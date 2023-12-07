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


@app.get("/users/new/")
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


@app.post("/users/new/")
def handle_new_user():
    """ Processes the new user add form and adds a User to the database

    Data needed to create a User instance:
        - first_name (str): Submitted first name from form (required)
        - last_name  (str): Submitted last name from form (required)
        - image_url  (str): Submited profile image url (optional)

    Returns a redirect back to the /users/ endpoint
    """

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    image_url = str(image_url) if image_url else ""

    user = User(first_name=first_name,
                last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()
    # TODO: Flash success message? Remember to import flash
    return redirect("/users/")


@app.get("/users/<int:user_id>/")
def show_user_detail_page(user_id):
    """ Shows the page of information of a given user.
        Contains options to edit or delete user profile.

        Returns:
            user_details.html template
            user object with the corresponding id
    """

    user = User.query.get_or_404(user_id)
    print("user instance: ", user)

    return render_template("user_details.html", user=user)

# TODO: Handle routing for GET /users/[user-id]/edit
# will require new template with form


@app.get("/users/<int:user_id>/edit/")
def show_user_edit_form(user_id):
    """"""
    user = User.query.get_or_404(user_id)

    return render_template("edit_user_form.html", user=user)

# TODO: Handle routing and logic for POST /users/[user-id]/edit


@app.post("/users/<int:user_id>/edit/")
def handle_user_edit_form(user_id):
    """"""

    user = User.query.get_or_404(user_id)

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url if image_url != "" else user.image_url

    db.session.add(user)
    db.session.commit()

    return redirect(f"/users/{user_id}/")

# TODO: Handle routing and logic for for POST /users/[user-id]/delete


# TODO: Add python tests to at least 4 of your routes


# TODO: Request Code Review
