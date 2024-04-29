#!/usr/bin/python3
<<<<<<< HEAD
"""Create a new view for User objects"""
from models import storage
from models.user import User
from api.v1.views import app_views
from flask import jsonify, abort, request
from flasgger.utils import swag_from


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/user/all_users.yml', methods=['GET'])
def users():
    """Get all stored users"""
    res = [
        user.to_dict() for user in storage.all(User).values()
    ]
    return jsonify(res)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/user/get_user.yml', methods=['GET'])
def user_by_id(user_id):
    """Get a User object by id"""
    res = storage.get(User, user_id)
    if res is None:
        abort(404)
    return jsonify(res.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/user/delete_user.yml', methods=['DELETE'])
def delete_user(user_id):
    """Delete an User object by its id """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({})


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/user/post_user.yml', methods=['POST'])
def insert_user():
    """Insert a new User object"""
    body = request.get_json()
    if type(body) != dict:
        return abort(400, {'message': 'Not a JSON'})
    if 'email' not in body:
        return abort(400, {'message': 'Missing email'})
    if 'password' not in body:
        return abort(400, {'message': 'Missing password'})
    new_user = User(**body)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
@swag_from('documentation/user/put_user.yml', methods=['PUT'])
def update_user_by_id(user_id):
    """Update an User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    body = request.get_json()
    if type(body) != dict:
        return abort(400, {'message': 'Not a JSON'})
    for key, value in body.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
=======
"""This module creates a users view"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User
from datetime import datetime
import uuid


@app_views.route('/users/', methods=['GET'])
@app_views.route('/users', methods=['GET'])
def list_users():
    list_users = [obj.to_dict() for obj in storage.all("User").values()]
    return jsonify(list_users)


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    all_users = storage.all("User").values()
    user_obj = [obj.to_dict() for obj in all_users if obj.id == user_id]
    if user_obj == []:
        abort(404)
    return jsonify(user_obj[0])


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    all_users = storage.all("User").values()
    user_obj = [obj.to_dict() for obj in all_users if obj.id == user_id]
    if user_obj == []:
        abort(404)
    user_obj.remove(user_obj[0])
    for obj in all_users:
        if obj.id == user_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200


@app_views.route('/users/', methods=['POST'])
def create_user():
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'email' not in request.get_json():
        abort(400, 'Missing name')
    if 'password' not in request.get_json():
        abort(400, 'Missing name')
    users = []
    new_user = User(email=request.json['email'],
                    password=request.json['password'])
    storage.new(new_user)
    storage.save()
    users.append(new_user.to_dict())
    return jsonify(users[0]), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def updates_user(user_id):
    """
    Update a user based on the given user_id.

    Args:
        user_id (str): The ID of the user to be updated.

    Returns:
        tuple: A tuple containing the
        updated user object and the HTTP status code.

    Raises:
        404: If the user with the given user_id is not found.
        400: If the request data is not in JSON format.

    """
    all_users = storage.all("User").values()
    user_obj = [obj.to_dict() for obj in all_users if obj.id == user_id]
    if user_obj == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    try:
        user_obj[0]['first_name'] = request.json['first_name']
    except Exception:
        pass
    try:
        user_obj[0]['last_name'] = request.json['last_name']
    except Exception:
        pass
    for obj in all_users:
        if obj.id == user_id:
            try:
                if request.json['first_name'] is not None:
                    obj.first_name = request.json['first_name']
            except Exception:
                pass
            try:
                if request.json['last_name'] is not None:
                    obj.last_name = request.json['last_name']
            except Exception:
                pass
    storage.save()
    return jsonify(user_obj[0]), 200
>>>>>>> 80d9ade6cc517ade851f78266dd8a0bf50694cda
