#!/usr/bin/python3
"""This module creates a place_amenities view"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.amenity import Amenity
from datetime import datetime
import uuid
from os import getenv

if getenv('HBNB_TYPE_STORAGE') == 'db':
    @app_views.route('/places/<place_id>/amenities', methods=['GET'])
    @app_views.route('/places/<place_id>/amenities/', methods=['GET'])
    def list_amenities_of_place(place_id):
        all_places = storage.all("Place").values()
        place_obj = [obj.to_dict() for obj in all_places if obj.id == place_id]
        if place_obj == []:
            abort(404)
        list_amenities = []
        for obj in all_places:
            if obj.id == place_id:
                for amenity in obj.amenities:
                    list_amenities.append(amenity.to_dict())
        return jsonify(list_amenities)

    @app_views.route('/places/<place_id>/amenities/<amenity_id>',
                     methods=['POST'])
    def create_place_amenity(place_id, amenity_id):
        """
        Create a new place-amenity relationship.

        Args:
            place_id (str): The ID of the place.
            amenity_id (str): The ID of the amenity.

        Returns:
            tuple: A tuple containing the JSON
            response and the HTTP status code.

        Raises:
            404: If the place or amenity does not exist.

        """
        all_places = storage.all("Place").values()
        place_obj = [obj.to_dict() for obj in all_places if obj.id == place_id]
        if place_obj == []:
            abort(404)

        all_amenities = storage.all("Amenity").values()
        amenity_obj = [obj.to_dict()
                       for obj in all_amenities if obj.id == amenity_id]
        if amenity_obj == []:
            abort(404)

        amenities = []
        for place in all_places:
            if place.id == place_id:
                for amenity in all_amenities:
                    if amenity.id == amenity_id:
                        place.amenities.append(amenity)
                        storage.save()
                        amenities.append(amenity.to_dict())
                        return jsonify(amenities[0]), 200
        return jsonify(amenities[0]), 201

    @app_views.route('/places/<place_id>/amenities/<amenity_id>',
                     methods=['DELETE'])
    def delete_place_amenity(place_id, amenity_id):
        all_places = storage.all("Place").values()
        place_obj = [obj.to_dict() for obj in all_places if obj.id == place_id]
        if place_obj == []:
            abort(404)

        all_amenities = storage.all("Amenity").values()
        amenity_obj = [obj.to_dict() for obj in all_amenities
                       if obj.id == amenity_id]
        if amenity_obj == []:
            abort(404)
        amenity_obj.remove(amenity_obj[0])

        for obj in all_places:
            if obj.id == place_id:
                if obj.amenities == []:
                    abort(404)
                for amenity in obj.amenities:
                    if amenity.id == amenity_id:
                        storage.delete(amenity)
                        storage.save()
        return jsonify({}), 200


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_place_amenity(amenity_id):
    all_amenities = storage.all("Amenity").values()
    amenity_obj = [obj.to_dict() for obj in all_amenities
                   if obj.id == amenity_id]
    if amenity_obj == []:
        abort(404)
    return jsonify(amenity_obj[0])
