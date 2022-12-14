
""" Flask web app tests """

import pytest
from flask import session
from ..web import create_app
from ..web.models import User

# FIXTURES ---------------------------------------------------

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "LOGIN_DISABLED": True
    })
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def user():
    return User("test_username", "test_password")

# TESTS ------------------------------------------------------

# auth

def test_get_login_page(client):
    # should get '/login'
    response = client.get("/login")
    assert response.request.path == "/login"

def test_get_logout_redirect(client):
    # should redirect to '/login'
    response = client.post("/logout", follow_redirects=True)
    assert response.request.path == "/login"

# routes

def test_get_index_page(client):
    # should get '/index'
    response = client.get("/index")
    assert response.request.path == "/index"

def test_get_index_page_without_logging(client):
    # should redirect to '/login'
    response = client.get("/index", follow_redirects=True)
    assert response.request.path == "/login"

def test_get_json_content_page(client):
    # should redirect to '/json_content'
    with client.session_transaction() as session:
        session["filter"] = None
    response = client.get("/json_content", follow_redirects=True)
    assert response.request.path == "/json_content"

def test_session_post_fill_bar_page_content_type(client):
    # 'todo_bar' variable shouldnt be in Session
    with client.session_transaction() as session:
        response = client.post("/fill_bar", data={
            "todo_input": "1 | test | TODO"
        })
    assert response.content_type == "text/html; charset=utf-8"

def test_post_index_page(client):
    # should return '405' (Method Not Allowed)
    response = client.post("/index", data={})
    assert response.status_code == 405

# queries

def test_get_add_page(client):
    # should return '405' (Method Not Allowed)
    response = client.get("/add", data={})
    assert response.status_code == 405

def test_get_delete_page(client):
    # should return '405' (Method Not Allowed)
    response = client.get("/delete", data={})
    assert response.status_code == 405

def test_get_update_page(client):
    # should return '405' (Method Not Allowed)
    response = client.get("/update", data={})
    assert response.status_code == 405

# models

def test_user_invalid_check_password_method(user):
    # should return False
    assert not user.check_password("invalid_password")

def test_user_valid_check_password_method(user):
    # should return True
    assert user.check_password("test_password")