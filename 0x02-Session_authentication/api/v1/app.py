#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def not_found(error) -> str:
    """ Unauthorized found handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def not_found(error) -> str:
    """ Forbidden found handler
    """
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def before_request_management():
    """ Managing before request """
    if auth is None:
        return
    ex_path = [
        '/api/v1/status/',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/',
        '/api/v1/auth_session/login/',
    ]
    if not auth.require_auth(path=request.path, excluded_paths=ex_path):
        return
    elif auth.authorization_header(request
                                   ) is None and auth.session_cookie(request
                                                                     ) is None:
        abort(401)
    elif auth.current_user(request=request) is None:
        abort(403)
    elif auth.authorization_header(request=request) is None:
        abort(401)
    else:
        request.current_user = auth.current_user(request=request)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    auth_type = getenv("AUTH_TYPE")
    if auth_type == 'basic_auth':
        from api.v1.auth.basic_auth import BasicAuth
        auth = BasicAuth()
    elif auth_type == 'session_auth':
        from api.v1.auth.session_auth import SessionAuth
        auth = SessionAuth()
    elif auth_type == 'auth':
        from api.v1.auth.auth import Auth
        auth = Auth()
    app.run(host=host, port=port)
