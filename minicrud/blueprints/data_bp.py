"""
This module defines the blueprint for the data-related endpoints.
"""

from flask import Blueprint, request, jsonify, current_app
from minicrud.database import db
from minicrud.models import Data
from minicrud.auth import token_required

data_bp = Blueprint('data_bp', __name__)

@data_bp.route('/data', methods=['POST'])
@token_required
def create_data(current_user):
    """
    Creates a new data entry.

    This endpoint allows an authenticated user to create a new data entry.
    The text for the new data is provided in the JSON body of the request.

    Args:
        current_user (User): The user object of the authenticated user.

    Returns:
        A JSON response indicating the success or failure of the operation.
    """
    data = request.get_json()
    new_data = Data(text=data['text'], user_id=current_user.id)
    db.session.add(new_data)
    db.session.commit()
    current_app.logger.info(f"User {current_user.username} created new data with id {new_data.id}")
    return jsonify({'message': 'New data created!'})

@data_bp.route('/data', methods=['GET'])
@token_required
def get_all_data(current_user):
    """
    Retrieves all data entries.

    This endpoint returns a list of all data entries for the authenticated user.

    Args:
        current_user (User): The user object of the authenticated user.

    Returns:
        A JSON response containing a list of all data entries.
    """
    datas = Data.query.filter_by(editor=current_user.username).all()
    output = []
    for data in datas:
        data_data = {}
        data_data['id'] = data.id
        data_data['text'] = data.text
        data_data['last_modified'] = data.last_modified
        data_data['editor'] = data.editor
        output.append(data_data)
    current_app.logger.info(f"User {current_user.username} retrieved all data.")
    return jsonify({'data': output})

@data_bp.route('/data/<data_id>', methods=['GET'])
@token_required
def get_one_data(current_user, data_id):
    """
    Retrieves a single data entry by its ID.

    This endpoint returns a single data entry that matches the provided data_id.

    Args:
        current_user (User): The user object of the authenticated user.
        data_id (int): The ID of the data entry to retrieve.

    Returns:
        A JSON response containing the requested data entry.
    """
    data = Data.query.filter_by(id=data_id, editor=current_user.username).first()
    if not data:
        current_app.logger.warning(f"User {current_user.username} failed to retrieve data with id {data_id}.")
        return jsonify({'message': 'No data found!'})
    data_data = {}
    data_data['id'] = data.id
    data_data['text'] = data.text
    data_data['last_modified'] = data.last_modified
    data_data['editor'] = data.editor
    current_app.logger.info(f"User {current_user.username} retrieved data with id {data_id}.")
    return jsonify(data_data)

@data_bp.route('/data/<data_id>', methods=['PUT'])
@token_required
def update_data(current_user, data_id):
    """
    Updates an existing data entry.

    This endpoint allows an authenticated user to update an existing data entry
    by its ID. The new text is provided in the JSON body of the request.

    Args:
        current_user (User): The user object of the authenticated user.
        data_id (int): The ID of the data entry to update.

    Returns:
        A JSON response indicating the success of the operation.
    """
    data = Data.query.filter_by(id=data_id, editor=current_user.username).first()
    if not data:
        current_app.logger.warning(f"User {current_user.username} failed to update data with id {data_id}.")
        return jsonify({'message': 'No data found!'})
    text = request.get_json()['text']
    data.text = text
    db.session.commit()
    current_app.logger.info(f"User {current_user.username} updated data with id {data_id}.")
    return jsonify({'message': 'Data has been updated!'})

@data_bp.route('/data/<data_id>', methods=['DELETE'])
@token_required
def delete_data(current_user, data_id):
    """
    Deletes a data entry.

    This endpoint allows an authenticated user to delete a data entry by its ID.

    Args:
        current_user (User): The user object of the authenticated user.
        data_id (int): The ID of the data entry to delete.

    Returns:
        A JSON response indicating the success of the operation.
    """
    data = Data.query.filter_by(id=data_id, editor=current_user.username).first()
    if not data:
        current_app.logger.warning(f"User {current_user.username} failed to delete data with id {data_id}.")
        return jsonify({'message': 'No data found!'})
    db.session.delete(data)
    db.session.commit()
    current_app.logger.info(f"User {current_user.username} deleted data with id {data_id}.")
    return jsonify({'message': 'Data has been deleted!'})
