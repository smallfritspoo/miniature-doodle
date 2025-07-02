"""
This module defines the database models for the minicrud application.
"""

from minicrud.database import db
import datetime

class User(db.Model):
    """
    Represents a user in the database.

    Attributes:
        id (int): The primary key for the user.
        username (str): The user's username.
        email (str): The user's email address.
        password_hash (str): The user's hashed password.
        api_token (str): The user's REST API token.
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    api_token = db.Column(db.String(128), unique=True)

    def __repr__(self):
        return f'<User {self.username}>'

class Data(db.Model):
    """
    Represents a data entry in the database.

    Attributes:
        id (int): The primary key for the data entry.
        text (str): The text content of the entry.
        last_modified (datetime): The timestamp of the last modification.
        user_id (int): The foreign key of the user who last edited the entry.
        editor (User): The relationship to the User model.
    """
    __tablename__ = 'data'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    last_modified = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    editor = db.relationship('User', backref=db.backref('data_entries', lazy=True))

    def __repr__(self):
        return f'<Data {self.id}>'
