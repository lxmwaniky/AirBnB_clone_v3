#!/usr/bin/python3
"""This module creates a blueprint for the API views."""
from api.v1.views import app_views
from flask import jsonify
from models import storage


classes = {"users": "User", "places": "Place", "states": "State",
           "cities": "City", "amenities": "Amenity",
           "reviews": "Review"}


@app_views.route('/status', methods=['GET'])
def status():
    ''' routes to status page '''
    return jsonify({'status': 'OK'})


@app_views.route('/stats', methods=['GET'])
def count():
    '''Retrieves the number of each object by type.

    This function counts the number of objects for
    each class in the 'classes' dictionary
    and returns a JSON response with the count for each object type.

    Returns:
        A JSON response containing the count of each object type.
    '''
    count_dict = {}
    for cls in classes:
        count_dict[cls] = storage.count(classes[cls])
    return jsonify(count_dict)
