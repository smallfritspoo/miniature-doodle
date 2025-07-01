"""
This module handles authentication for the minicrud application.
"""

from functools import wraps
from flask import request, jsonify
from .models import User

def token_required(f):
    """
    Decorator to ensure that a valid token is present in the request headers.

    Args:
        f (function): The function to be decorated.

    Returns:
        function: The decorated function.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            user = User.query.filter_by(api_token=token).first()
            if not user:
                return jsonify({'message': 'Token is invalid!'}), 401
        except Exception as e:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(user, *args, **kwargs)

    return decorated
