"""
This module contains the main Flask application and defines the API routes.
"""

from flask import Flask, request, jsonify
from .config import Config
from .database import db
from .models import User, Data
from .auth import token_required


def create_app():
    """
    Creates and configures the Flask application.

    Returns:
        Flask: The configured Flask application.
    """
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    @app.route('/data', methods=['POST'])
    @token_required
    def create_data(current_user):
        """
        Creates a new data entry.

        Returns:
            Response: A JSON response indicating success or failure.
        """
        data = request.get_json()
        new_data = Data(text=data['text'], user_id=current_user.id)
        db.session.add(new_data)
        db.session.commit()
        return jsonify({'message': 'New data created!'})

    @app.route('/data', methods=['GET'])
    @token_required
    def get_all_data(current_user):
        """
        Retrieves all data entries.

        Returns:
            Response: A JSON response with all data entries.
        """
        data = Data.query.all()
        output = []
        for d in data:
            data_item = {}
            data_item['id'] = d.id
            data_item['text'] = d.text
            data_item['last_modified'] = d.last_modified
            data_item['editor'] = User.query.get(d.user_id).username
            output.append(data_item)
        return jsonify({'data': output})

    @app.route('/data/<data_id>', methods=['GET'])
    @token_required
    def get_one_data(current_user, data_id):
        """
        Retrieves a single data entry.

        Args:
            data_id (int): The ID of the data entry to retrieve.

        Returns:
            Response: A JSON response with the requested data entry.
        """
        data = Data.query.filter_by(id=data_id).first()
        if not data:
            return jsonify({'message': 'No data found!'})

        data_item = {}
        data_item['id'] = data.id
        data_item['text'] = data.text
        data_item['last_modified'] = data.last_modified
        data_item['editor'] = User.query.get(data.user_id).username
        return jsonify(data_item)

    @app.route('/data/<data_id>', methods=['PUT'])
    @token_required
    def update_data(current_user, data_id):
        """
        Updates a data entry.

        Args:
            data_id (int): The ID of the data entry to update.

        Returns:
            Response: A JSON response indicating success.
        """
        data = Data.query.filter_by(id=data_id).first()
        if not data:
            return jsonify({'message': 'No data found!'})

        json_data = request.get_json()
        data.text = json_data['text']
        data.user_id = current_user.id
        db.session.commit()
        return jsonify({'message': 'Data has been updated!'})

    @app.route('/data/<data_id>', methods=['DELETE'])
    @token_required
    def delete_data(current_user, data_id):
        """
        Deletes a data entry.

        Args:
            data_id (int): The ID of the data entry to delete.

        Returns:
            Response: A JSON response indicating success.
        """
        data = Data.query.filter_by(id=data_id).first()
        if not data:
            return jsonify({'message': 'No data found!'})

        db.session.delete(data)
        db.session.commit()
        return jsonify({'message': 'Data has been deleted!'})

    return app
