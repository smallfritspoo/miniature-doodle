"""
This module contains the factory function for creating the Flask application.
"""

from flask import Flask
from minicrud.database import db
from minicrud.config import Config
from minicrud.blueprints.data_bp import data_bp

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
    

    app.register_blueprint(data_bp)

    return app