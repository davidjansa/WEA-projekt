
"""  Web app database queries routes and functions """

from flask import Blueprint, redirect, url_for, request
from flask_login import login_required
from . import db
from .models import Todo

queries = Blueprint("queries", __name__)

@queries.route("/add", methods=["POST"])
@login_required
def add_todo():
    """Add new Todo into the database

    Returns:
        if new Todo was inserted into the database -> redirect to 'routes.clear_bar' page
        else -> redirect to 'routes.index' page
    """
    # get data from form
    todo_text = request.form.get("text_input")
    todo_done = bool(request.form.get("done_input") == "on")

    # if Todos text is empty -> redicrect to 'routes.index' page
    if todo_text == "":
        return redirect(url_for("routes.index"))

    # try-except block with rollback() function
    try:
        new_todo = Todo(text=todo_text, done=todo_done)
        db.session.add(new_todo)
        db.session.commit()
    except:
        db.session.rollback()

    return redirect(url_for("routes.clear_bar"))

@queries.route("/delete", methods=["POST"])
@login_required
def delete_todo():
    """Delete Todo from the database

    Returns:
        Redirect to 'routes.clear_bar' page
    """
    # get data from form
    form_id = request.form.get("index_input")

    # find specific Todo in database based on his id
    todo = Todo.query.filter(Todo._id == form_id)

    # try-except block with rollback() function
    try:
        if todo:
            todo.delete()
            db.session.commit()
    except:
        db.session.rollback()

    return redirect(url_for("routes.clear_bar"))

@queries.route("/update", methods=["POST"])
@login_required
def update_todo():
    """Update specific Todo in the database

    Returns:
        Redirect to 'routes.clear_bar' page
    """
    # get data from form
    form_id = request.form.get("index_input")
    form_text = request.form.get("text_input", None)
    form_done = bool(request.form.get("done_input"))

    # find specific Todo in database based on his id
    todo = Todo.query.filter(Todo._id == form_id).first()

    # try-except block with rollback() function
    try:
        if todo:
            # if text is not empty
            if form_text:
                todo.text = form_text
            todo.done = form_done
            db.session.commit()
    except:
        db.session.rollback()

    return redirect(url_for("routes.clear_bar"))

def select(filt):
    """Function for 'Select' query in database

    Args:
        filt (bool):
            True -> Select only done Todos
            False -> Select only undone Todos
            None -> Select all Todos

    Returns:
        Query object: Selected Todos from the database
    """
    if filt == None:
        return Todo.query.all()
    else:
        return Todo.query.filter(Todo.done == filt)     
