"""
This module contains the factory function for creating the Flask application.
"""

"""
This module contains the factory function for creating the Flask application.
"""

import logging
import os
from flask import Flask
from minicrud.config import Config
from minicrud.blueprints.data_bp import data_bp

def create_app():
    """
    Creates and configures a Flask application with logging.

    This function creates a new Flask application, configures it using the
    Config class, initializes the database, and registers the blueprints.
    It also sets up logging based on environment variables.

    Returns:
        The configured Flask application.
    """
    log_level = os.environ.get('LOG_LEVEL', 'DEBUG')
    log_file = os.environ.get('LOG_FILE', 'minicrud.log')
    log_format = os.environ.get('LOG_FORMAT', '%(asctime)s %(levelname)s %(message)s')

    logging.basicConfig(level=log_level,
                        filename=log_file,
                        format=log_format)
    
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Set up logging
    handler = logging.FileHandler(log_file)
    handler.setLevel(log_level)
    handler.setFormatter(logging.Formatter(log_format))
    app.logger.addHandler(handler)

    app.register_blueprint(data_bp)

    app.logger.info("Flask application created successfully.")
    return app