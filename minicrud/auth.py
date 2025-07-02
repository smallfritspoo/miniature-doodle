"""
This module handles authentication for the minicrud application.
"""

from functools import wraps
from flask import request, jsonify
from .models import User

from flask import current_app
import jwt

def token_required(f):
    """
    Decorator that checks for a valid JWT token in the request headers.

    This decorator ensures that the request has a valid 'x-access-token' header.
    It decodes the token to identify the user and passes the user object to the
    decorated function.

    Args:
        f (function): The function to be decorated.

    Returns:
        The decorated function or a JSON error response if authentication fails.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(id=data['id']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated
