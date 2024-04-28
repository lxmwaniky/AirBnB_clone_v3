#!/usr/bin/python3

"""This module handles routes for State objects."""

from flask import Response, jsonify, request, abort
from models.state import State
from models import storage
from api.v1.views import app_views


@app_views.route('/states', methods=['GET', 'POST'])
def handle_states() -> Response:
    """
    Handles GET and POST requests for states.

    Returns:
        Response: The response object containing the result of the request.
    """
    if request.method == 'POST':
        data = request.get_json(silent=True)

        # the data provided must be a dictionary
        if not data or not isinstance(data, dict):
            return "Not a JSON", 400

        if "name" not in data:
            return "Missing name", 400

        state_obj = State(**data)
        state_obj.save()

        return jsonify(state_obj.to_dict()), 201

    # default is GET
    return jsonify(
        [state.to_dict() for state in storage.all(State).values()]
    )


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'])
def handle_state(state_id: str | None = None) -> Response:
    """
    Handles GET, DELETE, and PUT requests for a specific state.

    Args:
        state_id (str): The ID of the state.

    Returns:
        Response: The response object containing the result of the request.
    """
    state_obj = storage.get(State, state_id)
    if not state_obj:
        abort(404)

    if request.method == 'DELETE':
        storage.delete(state_obj)
        return jsonify({}), 200

    if request.method == 'PUT':
        data = request.get_json(silent=True)

        # the data provided must be a dictionary
        if not data or not isinstance(data, dict):
            return "Not a JSON", 400

        if "name" not in data:
            return "Missing name", 400

        for key, value in data.items():
            if key in ['id', 'created_at', 'updated_at']:
                continue

            setattr(state_obj, key, value)

        state_obj.save()
        return jsonify(state_obj.to_dict()), 200

    # default method is GET
    return jsonify(state_obj.to_dict())
