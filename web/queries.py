from flask import Flask, Blueprint, render_template, redirect, url_for, request
from . import db
from .models import Todo, User

queries = Blueprint("queries", __name__)

@queries.route("/add", methods=["POST", "GET"])
def addTodo():
    todo_text = request.form.get("text_input")

    if todo_text == "":
        return redirect(url_for("routes.index"))

    new_todo = Todo(text=todo_text)
    db.session.add(new_todo)
    db.session.commit()

    return redirect(url_for("routes.index"))

@queries.route("/delete", methods=["POST", "GET"])
def deleteTodo():
    form_id = request.form.get("index_input")

    todo = Todo.query.filter(Todo._id == form_id)

    if todo:
        todo.delete()
        db.session.commit()

    return redirect(url_for("routes.index"))

@queries.route("/update", methods=["POST", "GET"])
def updateTodo():
    form_id = request.form.get("index_input")
    form_text = request.form.get("text_input")
    form_text = form_text if form_text else None
    form_done = True if request.form.get("done_input") else False

    todo = Todo.query.filter(Todo._id == form_id).first()

    if todo:
        if form_text:
            todo.text = form_text
        todo.done = form_done
        db.session.commit()

    return redirect(url_for("routes.index"))