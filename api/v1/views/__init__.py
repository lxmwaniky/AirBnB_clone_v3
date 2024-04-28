from flask import Blueprint
from api.v1.views.index import *

# Create an instance of Blueprint with the url prefix /api/v1
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Wildcard import of everything in the package api.v1.views.index