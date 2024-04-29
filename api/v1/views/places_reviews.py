#!/usr/bin/python3
<<<<<<< HEAD
"""This module implement a rule that return a view"""
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.review import Review
from models.place import Place
from models.user import User
from flasgger.utils import swag_from


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
@swag_from('documentation/reviews/get_reviews.yml', methods=['GET'])
def review_by_place(place_id):
    """View function that return Review objects by Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify([review.to_dict() for review in place.reviews])


@app_views.route("/reviews/<review_id>", methods=["GET"],
                 strict_slashes=False)
@swag_from('documentation/reviews/get_review.yml', methods=['GET'])
def show_review(review_id):
    """Endpoint that return a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", methods=["DELETE"],
                 strict_slashes=False)
@swag_from('documentation/reviews/delete_reviews.yml', methods=['DELETE'])
def delete_review(review_id):
    """Endpoint that delete a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({})


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
@swag_from('documentation/reviews/post_reviews.yml', methods=['POST'])
def insert_review(place_id):
    """Endpoint that insert a Review object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    res = request.get_json()
    if type(res) != dict:
        abort(400, description="Not a JSON")
    if not res.get("user_id"):
        abort(400, description="Missing user_id")
    res['place_id'] = place_id
    user = storage.get(User, res.get('user_id'))
    if user is None:
        abort(404)
    if not res.get("text"):
        abort(400, description="Missing text")
    new_review = Review(**res)
    new_review.place_id = place_id
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"],
                 strict_slashes=False)
@swag_from('documentation/reviews/put_reviews.yml', methods=['PUT'])
def update_review(review_id):
    """Endpoint that update a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    res = request.get_json()
    if type(res) != dict:
        abort(400, description="Not a JSON")
    for key, value in res.items():
        if key not in ["id", "user_id", "place_id",
                       "created_at", "updated_at"]:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200
=======
"""This module creates a places review view"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review
from datetime import datetime
import uuid


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
@app_views.route('/places/<place_id>/reviews/', methods=['GET'])
def list_reviews_of_place(place_id):
    all_places = storage.all("Place").values()
    place_obj = [obj.to_dict() for obj in all_places if obj.id == place_id]
    if place_obj == []:
        abort(404)
    list_reviews = [obj.to_dict() for obj in storage.all("Review").values()
                    if place_id == obj.place_id]
    return jsonify(list_reviews)


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    """
    Create a new review for a place.

    Args:
        place_id (str): The ID of the place.

    Returns:
        tuple: A tuple containing the JSON response and the HTTP status code.

    Raises:
        BadRequest: If the request body is not a valid
        JSON or if it is missing required fields.
        NotFound: If the place or user specified in the request does not exist.
    """
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'user_id' not in request.get_json():
        abort(400, 'Missing user_id')
    user_id = request.json['user_id']
    if 'text' not in request.get_json():
        abort(400, 'Missing text')
    all_places = storage.all("Place").values()
    place_obj = [obj.to_dict() for obj in all_places if obj.id == place_id]
    if place_obj == []:
        abort(404)
    all_users = storage.all("User").values()
    user_obj = [obj.to_dict() for obj in all_users if obj.id == user_id]
    if user_obj == []:
        abort(404)
    reviews = []
    new_review = Review(text=request.json['text'], place_id=place_id,
                        user_id=user_id)
    storage.new(new_review)
    storage.save()
    reviews.append(new_review.to_dict())
    return jsonify(reviews[0]), 201


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    all_reviews = storage.all("Review").values()
    review_obj = [obj.to_dict() for obj in all_reviews if obj.id == review_id]
    if review_obj == []:
        abort(404)
    return jsonify(review_obj[0])


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    all_reviews = storage.all("Review").values()
    review_obj = [obj.to_dict() for obj in all_reviews if obj.id == review_id]
    if review_obj == []:
        abort(404)
    review_obj.remove(review_obj[0])
    for obj in all_reviews:
        if obj.id == review_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def updates_review(review_id):
    all_reviews = storage.all("Review").values()
    review_obj = [obj.to_dict() for obj in all_reviews if obj.id == review_id]
    if review_obj == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'text' in request.get_json():
        review_obj[0]['text'] = request.json['text']
        for obj in all_reviews:
            if obj.id == review_id:
                obj.text = request.json['text']
        storage.save()
    return jsonify(review_obj[0]), 200
>>>>>>> 80d9ade6cc517ade851f78266dd8a0bf50694cda
