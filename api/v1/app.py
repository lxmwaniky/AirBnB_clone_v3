#!/usr/bin/python3
""" model - flask app """
from os import environ
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_db(error):
    """teardown app"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ handling 404 error"""
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    """main function """
    host = environ.get('HBNB_API_HOST')
    port = environ.get('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)