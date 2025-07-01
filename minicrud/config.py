"""
This module contains the configuration settings for the minicrud application.

It loads sensitive information and database configurations from environment
variables.
"""

import os

class Config:
    """
    Configuration class for the Flask application.

    Attributes:
        SQLALCHEMY_DATABASE_URI (str): The database URI for SQLAlchemy.
        SQLALCHEMY_TRACK_MODIFICATIONS (bool): Whether to track modifications.
        SECRET_KEY (str): The secret key for the application.
    """
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY")
