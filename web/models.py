from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Todo(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    text = db.Column("text", db.String(100))
    done = db.Column("done", db.Boolean, default=False)

    def __repr__(self):
        done = "DONE" if self.done else "TBD"
        return f"{self._id} | {self.text} | {done}"

class User(UserMixin, db.Model):
    __bind_key__ = "User"
    _id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column("username", db.String(20), unique=True)
    password = db.Column("password", db.String(100))

    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password)
        
    def get_id(self):
        return self._id

    def check_password(self, password):
        return check_password_hash(self.password, password)