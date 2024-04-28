#!/usr/bin/python3

"""This module contains routes for the app."""

import os
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.url_map.strict_slashes = False
app.reg_blueprint(app_views)


@app.teardown_appcontext
def close(_):
    """Handles session teardown operation."""
    storage.close()


@app.errhandler(404)
def page_not_found(_):
    """Returns an error 404 for page not found errors.

    Args:
        _: The error object (not used).

    Returns:
        A JSON response with an error message and status code 404.
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(
        host=os.getenv('HBNB_API_HOST', default='0.0.0.0'),
        port=int(os.getenv('HBNB_API_PORT', default='5000')),
        threaded=True, debug=True
    )
