
"""  Web app authorization routes """

from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import login_user, logout_user
from .models import User
from . import login

auth = Blueprint("auth", __name__)

@login.user_loader
def load_user(_id):
    """User lodaer

    Args:
        _id (int): User id

    Returns:
        User: Specific user with id == _id
    """
    return User.query.get(int(_id))

@auth.route("/login", methods=["GET"])
def login():
    """Login page

    Returns:
        Render 'login.html' template
    """
    return render_template("login.html")

@auth.route("/login", methods=["POST"])
def login_post():
    """Login User

    Returns:
        if data from form are valid -> redirect to 'routes.index' page
        else -> redirect to (same) 'auth.login' page
    """
    # get data from form
    form_username = request.form.get("username_input")
    form_password = request.form.get("password_input")

    # get User with specific username in database
    user = User.query.filter_by(username=form_username).first()

    # if User is not valid -> redirect to (same)'auth.login' page
    if not user or not user.check_password(form_password):
        flash("Invalid username or password")
        return redirect(url_for("auth.login"))

    # if User is valid -> login user in app session and redirect to 'routes.index' page
    login_user(user, remember=False)

    return redirect(url_for("routes.index"))

@auth.route("/logout", methods=["POST"])
def logout():
    """Loggout current user from app session

    Returns:
        Redirect to 'auth.login' page
    """
    logout_user()
    session.clear()
    return redirect(url_for("auth.login"))
