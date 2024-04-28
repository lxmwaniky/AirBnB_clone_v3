#!/usr/bin/python3

from flask import Flask, Blueprint
from models import storage

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *


def create_app():
    app = Flask(__name__)
    app.register_blueprint(app_views)

    @app.teardown_appcontext
    def close_storage(exception):
        """Closes the storage"""
        storage.close()

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, threaded=True)
