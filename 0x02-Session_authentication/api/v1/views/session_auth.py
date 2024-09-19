#!/usr/bin/env python3
""" Session Authentication views
"""
import os
from flask import jsonify, request
from api.v1.views import app_views
from api.v1.views.users import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login_request() -> str:
    """ GET /api/v1/auth_session/login
    Return:
      - authentication of the API
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None or len(email) == 0:
        return jsonify({'error': 'email missing'}), 400
    if password is None or len(password) == 0:
        return jsonify({'error': 'password missing'}), 400
    users = User.search(attributes={'email': email})
    if users is None or len(users) == 0:
        return jsonify({'error': 'no user found for this email'}), 404
    user = users[0]
    if user.is_valid_password(password):
        return jsonify({'error', 'wrong password'}), 401
    else:
        from api.v1.app import auth
        sess_id = auth.create_session(user_id=user.id)
        auth.session_cookie(request=request)
        resp = jsonify(user.to_json())
        resp.set_cookie(os.getenv('SESSION_NAME'), sess_id)
        return resp
