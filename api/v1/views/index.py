#!/usr/bin/python3
"""module - index file"""
from models import storage
from flask import jsonify, Blueprint
from api.v1.views import app_views

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status_code():
    """return status code"""
    return jsonify({"status": "OK"})

@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def count_objects():
    """ count the number of objects in each class"""
    classes = ['State', 'City', 'Amenity', 'Place', 'Review', 'User']
    names = ['states', 'cities', 'amenities', 'places', 'review', 'users']

    objects = {}
    for i in range(len(classes)):
        objects[names[i]] = storage.count(classes[i])

    return jsonify(objects)