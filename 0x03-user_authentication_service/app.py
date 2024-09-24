#!/usr/bin/env python3
""" Our Flask module as we like it
"""
from flask import Flask, abort, jsonify, redirect, request, session
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route("/", methods=["GET"], strict_slashes=False)
def index():
    """ Here the index route """
    return jsonify({'message': 'Bienvenue'}), 200


@app.route("/users", methods=["POST"], strict_slashes=False)
def register():
    """ Endpoint for registering a user """
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        user = AUTH.register_user(email=email, password=password)
        return jsonify({
            'email': '{}'.format(user.email),
            'message': 'user created'
        }), 200
    except ValueError:
        return jsonify({'message': 'email already registered'}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """ Login user with given data """
    email = request.form.get("email")
    password = request.form.get("password")
    if AUTH.valid_login(email=email, password=password):
        session_id = AUTH.create_session(email=email)
        response = jsonify({
            'email': '{}'.format(email),
            'message': 'logged in'
        })
        response.set_cookie("session_id", session_id, expires=None)
        return response, 200
    else:
        abort(401)


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """ Login out the user """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id=session_id)
    if user is not None:
        AUTH.destroy_session(user_id=user.id)
        return redirect('/')
    else:
        abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """ Let's collect the user's profile """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id=session_id)
    if user is not None:
        return jsonify({'email': '{}'.format(user.email)}), 200
    else:
        abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """ Getting the reset password token """
    email = request.form.get("email")
    try:
        token = AUTH.get_reset_password_token(email=email)
        return jsonify({'email': email, 'reset_token': token}), 200
    except Exception:
        abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password():
    """ Updating password """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    try:
        AUTH.update_password(reset_token=reset_token, password=new_password)
        return jsonify({'email': email, 'message': 'Password updated'}), 200
    except Exception:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
