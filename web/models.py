
"""  Web app database models """

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

class Todo(db.Model):
    """Defined database 'Todo' model

    Cols:
        _id (int): Todo index (primary_key)
        text (str): Todo text
        done (bool): Todo bool (done or to be done) = False

    Args:
        db (SQLAlchemy): Connected database

    Returns:
        Database 'Todo' model
    """
    _id = db.Column("id", db.Integer, primary_key=True)
    text = db.Column("text", db.String(100))
    done = db.Column("done", db.Boolean, default=False)

    def __repr__(self):
        done = "DONE" if self.done else "TBD"
        return f"{self._id} | {self.text} | {done}"

    def to_dict(self):
        return dict(id=self._id, text=self.text, done=self.done)

class User(UserMixin, db.Model):
    """Defined database 'User' model

    Cols:
        _id (int): User index (primary_key)
        username (str): User username (unique)
        password (str): User password

    Args:
        UserMixin (flask_login): Configuration with authentication
        db (SQLAlchemy): Connected database

    Returns:
        Database 'User' model
    """
    __bind_key__ = "User"
    _id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column("username", db.String(20), unique=True)
    password = db.Column("password", db.String(50))

    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password)

    def get_id(self):
        """Return Users id

        Returns:
            int: Users id
        """
        return self._id

    def check_password(self, password):
        """Check if inserted password is valid

        Args:
            password (str): Password to be checked

        Returns:
            bool: Compare valid password from database with inserted password
        """
        return check_password_hash(self.password, password)
