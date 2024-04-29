#!/usr/bin/python3
<<<<<<< HEAD
"""New view for the link between Place objects and Amenity objects"""
from models.place import Place
from models.amenity import Amenity
from api.v1.views import app_views
from models import storage
from os import getenv
from flask import jsonify, abort
from flasgger.utils import swag_from

mode = getenv("HBNB_TYPE_STORAGE")


@app_views.route("/places/<place_id>/amenities", methods=["GET"],
                 strict_slashes=False)
@swag_from('documentation/place_amenity/get_places_amenities.yml',
           methods=['GET'])
def amenities_from_place(place_id):
    """Get all amenities of a place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if mode == "db":
        return jsonify([amenity.to_dict() for amenity in place.amenities])
    else:
        return jsonify([
            storage.get(Amenity, _id).to_dict() for _id in place.amenity_ids
        ])


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"], strict_slashes=False)
@swag_from('documentation/place_amenity/delete_place_amenities.yml',
           methods=['DELETE'])
def delete_amenity_from_place(place_id, amenity_id):
    """Delete a Amenity object by its id from a Place object"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)
    if mode == "db":
        if amenity not in place.amenities:
            abort(404)
    else:
        if amenity.id not in place.amenity_id:
            abort(404)
    amenity.delete()
    storage.save()

    return jsonify({})


@app_views.route("places/<place_id>/amenities/<amenity_id>", methods=["POST"],
                 strict_slashes=False)
@swag_from('documentation/place_amenity/post_place_amenities.yml',
           methods=['POST'])
def insert_amenity_in_place(place_id, amenity_id):
    """Insert new amenity object into Place object"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)
    if mode == "db":
        if amenity in place.amenities:
            return jsonify(amenity.to_dict())
        else:
            place.amenities.append(amenity)
    else:
        if amenity.id in place.amenity_id:
            return jsonify(amenity.to_dict())
        else:
            place.amenity_id.append(amenity.id)
    storage.save()
    return jsonify(amenity.to_dict()), 201
=======
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
>>>>>>> 80d9ade6cc517ade851f78266dd8a0bf50694cda
