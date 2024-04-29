#!/usr/bin/python3
<<<<<<< HEAD
"""This module implement a rule that return a view"""
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.city import City
from models.place import Place
from models.user import User
from models.state import State
from models.amenity import Amenity
from flasgger.utils import swag_from


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
@swag_from('documentation/place/get_places.yml', methods=['GET'])
def place_by_city(city_id):
    """View function that return place objects by city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route("/places/<place_id>", methods=["GET"],
                 strict_slashes=False)
@swag_from('documentation/place/get_place.yml', methods=['GET'])
def show_place(place_id):
    """Endpoint that return a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
@swag_from('documentation/place/delete_place.yml', methods=['DELETE'])
def delete_place(place_id):
    """Endpoint that delete a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({})


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
@swag_from('documentation/place/post_place.yml', methods=['POST'])
def insert_place(city_id):
    """Endpoint that insert a Place object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    res = request.get_json()
    if type(res) != dict:
        abort(400, description="Not a JSON")
    if not res.get("user_id"):
        abort(400, description="Missing user_id")
    user = storage.get(User, res.get("user_id"))
    if user is None:
        abort(404)
    if not res.get("name"):
        abort(400, description="Missing name")
    new_place = Place(**res)
    new_place.city_id = city_id
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route("/places_search", methods=["POST"],
                 strict_slashes=False)
@swag_from('documentation/place/put_place.yml', methods=['PUT'])
def places_search():
    """Retrieves all Place objects depending of the body of the request"""
    body = request.get_json()
    if type(body) != dict:
        abort(400, description="Not a JSON")
    id_states = body.get("states", [])
    id_cities = body.get("cities", [])
    id_amenities = body.get("amenities", [])
    places = []
    if id_states == id_cities == []:
        places = storage.all(Place).values()
    else:
        states = [
            storage.get(State, _id) for _id in id_states
            if storage.get(State, _id)
        ]
        cities = [city for state in states for city in state.cities]
        cities += [
            storage.get(City, _id) for _id in id_cities
            if storage.get(City, _id)
        ]
        cities = list(set(cities))
        places = [place for city in cities for place in city.places]

    amenities = [
        storage.get(Amenity, _id) for _id in id_amenities
        if storage.get(Amenity, _id)
    ]

    res = []
    for place in places:
        res.append(place.to_dict())
        for amenity in amenities:
            if amenity not in place.amenities:
                res.pop()
                break

    return jsonify(res)


@app_views.route("/places/<place_id>", methods=["PUT"],
                 strict_slashes=False)
@swag_from('documentation/place/post_search.yml', methods=['POST'])
def update_place(place_id):
    """Endpoint that update a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    res = request.get_json()
    if type(res) != dict:
        abort(400, description="Not a JSON")
    for key, value in res.items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
=======
"""This module creates a places view."""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.place import Place
from datetime import datetime
import uuid


@app_views.route('/cities/<city_id>/places', methods=['GET'])
@app_views.route('/cities/<city_id>/places/', methods=['GET'])
def list_places_of_city(city_id):
    '''Retrieves a list of all Place objects in city'''
    all_cities = storage.all("City").values()
    city_obj = [obj.to_dict() for obj in all_cities if obj.id == city_id]
    if city_obj == []:
        abort(404)
    list_places = [obj.to_dict() for obj in storage.all("Place").values()
                   if city_id == obj.city_id]
    return jsonify(list_places)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    all_places = storage.all("Place").values()
    place_obj = [obj.to_dict() for obj in all_places if obj.id == place_id]
    if place_obj == []:
        abort(404)
    return jsonify(place_obj[0])


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    '''Deletes a Place object'''
    all_places = storage.all("Place").values()
    place_obj = [obj.to_dict() for obj in all_places
                 if obj.id == place_id]
    if place_obj == []:
        abort(404)
    place_obj.remove(place_obj[0])
    for obj in all_places:
        if obj.id == place_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    '''Creates a Place'''
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'user_id' not in request.get_json():
        abort(400, 'Missing user_id')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    all_cities = storage.all("City").values()
    city_obj = [obj.to_dict() for obj in all_cities
                if obj.id == city_id]
    if city_obj == []:
        abort(404)
    places = []
    new_place = Place(name=request.json['name'],
                      user_id=request.json['user_id'], city_id=city_id)
    all_users = storage.all("User").values()
    user_obj = [obj.to_dict() for obj in all_users
                if obj.id == new_place.user_id]
    if user_obj == []:
        abort(404)
    storage.new(new_place)
    storage.save()
    places.append(new_place.to_dict())
    return jsonify(places[0]), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def updates_place(place_id):
    """
    Update a place based on its ID.

    Args:
        place_id (str): The ID of the place to be updated.

    Returns:
        tuple: A tuple containing the JSON
        representation of the updated place and the HTTP status code.

    Raises:
        404: If the place with the given ID does not exist.
        400: If the request data is not in JSON format.

    """
    all_places = storage.all("Place").values()
    place_obj = [obj.to_dict() for obj in all_places if obj.id == place_id]
    if place_obj == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' in request.get_json():
        place_obj[0]['name'] = request.json['name']
    if 'description' in request.get_json():
        place_obj[0]['description'] = request.json['description']
    if 'number_rooms' in request.get_json():
        place_obj[0]['number_rooms'] = request.json['number_rooms']
    if 'number_bathrooms' in request.get_json():
        place_obj[0]['number_bathrooms'] = request.json['number_bathrooms']
    if 'max_guest' in request.get_json():
        place_obj[0]['max_guest'] = request.json['max_guest']
    if 'price_by_night' in request.get_json():
        place_obj[0]['price_by_night'] = request.json['price_by_night']
    if 'latitude' in request.get_json():
        place_obj[0]['latitude'] = request.json['latitude']
    if 'longitude' in request.get_json():
        place_obj[0]['longitude'] = request.json['longitude']
    for obj in all_places:
        if obj.id == place_id:
            if 'name' in request.get_json():
                obj.name = request.json['name']
            if 'description' in request.get_json():
                obj.description = request.json['description']
            if 'number_rooms' in request.get_json():
                obj.number_rooms = request.json['number_rooms']
            if 'number_bathrooms' in request.get_json():
                obj.number_bathrooms = request.json['number_bathrooms']
            if 'max_guest' in request.get_json():
                obj.max_guest = request.json['max_guest']
            if 'price_by_night' in request.get_json():
                obj.price_by_night = request.json['price_by_night']
            if 'latitude' in request.get_json():
                obj.latitude = request.json['latitude']
            if 'longitude' in request.get_json():
                obj.longitude = request.json['longitude']
    storage.save()
    return jsonify(place_obj[0]), 200
>>>>>>> 80d9ade6cc517ade851f78266dd8a0bf50694cda
