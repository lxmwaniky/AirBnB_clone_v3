from flask import Blueprint
from api.v1.views.index import *

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

"""
This module defines the blueprint for the API views.

The `app_views` blueprint is used to group related API endpoints together
under the `/api/v1` URL prefix. It provides a way to organize and modularize
the API routes.

Attributes:
    app_views (Blueprint): The Flask blueprint object for the API views.
"""
