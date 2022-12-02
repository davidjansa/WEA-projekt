from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user, logout_user
from . import login
from .models import Todo, User

routes = Blueprint("routes", __name__)

@routes.route('/')
@routes.route("/index", methods=["GET"])
def index():
    if current_user.is_authenticated:
        data = Todo.query.all()
        return render_template("index.html", data=data)
    return redirect(url_for("routes.login"))

# AUTH ---------------------------------------------------------------------

@login.user_loader
def load_user(_id):
    return User.query.get(int(_id))

@routes.route("/login", methods=["GET"])
def login():
    return render_template("login.html")

@routes.route("/login", methods=["POST", "GET"])
def login_post():
    form_username = request.form.get("username_input")
    form_password = request.form.get("password_input")

    user = User.query.filter_by(username=form_username).first()

    if not user or not user.check_password(form_password):
        #! flashnout message flash("Invalid username or password")
        return redirect(url_for("routes.login"))

    login_user(user, remember=False)

    return redirect(url_for("routes.index"))

@routes.route("/logout", methods=["POST", "GET"])
def logout():
    logout_user()
    return redirect(url_for("routes.login"))