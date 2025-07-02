"""
This module contains the factory function for creating the Flask application.
"""

from flask import Flask
from ..database import db
from ..config import Config
from .blueprints.data_bp import data_bp

def create_app():
    """
    Creates and configures a Flask application.

    This function creates a new Flask application, configures it using the
    Config class, initializes the database, and registers the blueprints.

    Returns:
        The configured Flask application.
    """
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    app.register_blueprint(data_bp)

    return app