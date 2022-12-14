
""" Web app main routes """

from flask import Blueprint, render_template, redirect, url_for, request, session, jsonify
from flask_login import current_user, login_required
from .queries import select

routes = Blueprint("routes", __name__)

# MAIN  --------------------------------------------------------------------

@routes.route('/')
@routes.route("/index", methods=["GET"])
def index():
    """Main page renderer

    Returns:
        if user is authenticated -> render 'index.html' template
        else -> redirect to 'auth.login' page
    """
    # check if user is logged
    if current_user.is_authenticated:
        # done/todo filter
        session["filter"] = session.get("filter", None)
        # todo_bar fill
        todo_bar = session.get("todo_bar", None)
        # get filtered data from database
        data = select(session["filter"])
        # send data
        return render_template("index.html", data=data, todo_bar=todo_bar)
    # return to login page
    return redirect(url_for("auth.login"))

# CONTENT ------------------------------------------------------------------

@routes.route("/json_content", methods=["POST", "GET"])
@login_required
def json_content():
    """Create from FILTERED data json content

    Returns:
        Redirect to 'routes.json_content' page with json data
    """
    data = [t.to_dict() for t in select(session["filter"])]
    return jsonify(data)

# FILTER -------------------------------------------------------------------

@routes.route("/filters", methods=["POST"])
@login_required
def filters():
    """Session 'filter' variable setup

    Returns:
        Redirect to 'routes.clear_bar' page
    """
    if session["filter"] is None:
        session["filter"] = True
    elif session["filter"] is True:
        session["filter"] = False
    else:
        session["filter"] = None
    return redirect(url_for("routes.clear_bar"))

# BAR  ---------------------------------------------------------------------

@routes.route("/clear_bar", methods=["POST", "GET"])
@login_required
def clear_bar():
    """Delete Session 'todo_bar' variable

    Returns:
        Redirect to 'routes.index' page
    """
    if "todo_bar" in session:
        session.pop("todo_bar")
    return redirect(url_for("routes.index"))


@routes.route("/fill_bar", methods=["POST"])
@login_required
def fill_bar():
    """Fill new data into Session 'todo_bar' variable

    Returns:
        if data from form are valid -> add data into Session and redirect to 'routes.index' page
        else -> redirect to 'routes.index' page
    """
    # get data from clicked todo card
    if request.form.get("todo_input"):
        form_get = request.form.get("todo_input").replace(" ", "").split('|')
    else:
        return redirect(url_for("routes.index"))

    # check length
    if len(form_get) != 3:
        return redirect(url_for("routes.index"))

    # check 'done' value
    if form_get[2] not in ["DONE", "TBD"]:
        return redirect(url_for("routes.index"))

    # data into session variable "todo_bar"
    todo_bar = {
        "_id": form_get[0],
        "text": form_get[1],
        "done": form_get[2]
    }

    session["todo_bar"] = todo_bar

    return redirect(url_for("routes.index"))
