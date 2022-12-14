
""" Flask web app configuration """

from datetime import timedelta
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login = LoginManager()

def create_app():
    """Flask app basic configuration

    Returns:
        app (Flask): Flask app
    """
    app = Flask(__name__, template_folder="../templates", static_folder="../static")

    # app configuration
    app.config["SECRET_KEY"] = "0b6b299e6aa023098522c70c1f2018154fcd2487c436655b4ead47aca87670d3"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Todo.sqlite"
    app.config["SQLALCHEMY_BINDS"] = {"User": "sqlite:///User.sqlite"}
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # remove warnings
    app.permanent_session_lifetime = timedelta(minutes=5)

    # init app
    db.init_app(app)

    # init login manager
    login.init_app(app)

    # blueprint for routes
    from .routes import routes as routes_blueprint
    app.register_blueprint(routes_blueprint, url_prefix="/")

    # blueprint for queries
    from .queries import queries as queries_blueprint
    app.register_blueprint(queries_blueprint, url_prefix="/")

    # blueprint for auth
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix="/")

    # init database
    init_db(app)

    return app

def init_db(app):
    """Initial database establishment

    Args:
        app (Flask): Flask app
    """
    with app.app_context():
        db.create_all()
