#!/usr/bin/env python3
"""
Main file
"""
import requests


def register_user(email: str, password: str) -> None:
    """ Here the function """
    url = 'http://localhost:5000/users'
    data = {'email': email, 'password': password}
    response = requests.post(url=url, data=data)

    if response.status_code == 200:
        assert response.status_code == 200
        assert response.json() == {'email': email, 'message': 'user created'}
    else:
        assert response.status_code == 400
        assert response.json() == {'message': 'email already registered'}


def log_in_wrong_password(email: str, password: str) -> None:
    """ Here the function """
    url = 'http://localhost:5000/sessions'
    data = {'email': email, 'password': password}
    response = requests.post(url=url, data=data)
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """ Here the function """
    url = 'http://localhost:5000/sessions'
    data = {'email': email, 'password': password}
    response = requests.post(url=url, data=data)
    assert response.status_code == 200
    assert response.json() == {'email': email, 'message': 'logged in'}
    assert response.cookies['session_id'] is not None
    return response.cookies['session_id']


def profile_unlogged() -> None:
    """ Here the function """
    url = 'http://localhost:5000/profile'
    response = requests.get(url=url)
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """ Here the function """
    url = 'http://localhost:5000/profile'
    response = requests.get(url=url, cookies={'session_id': session_id})
    assert response.status_code == 200


def log_out(session_id: str) -> None:
    """ Here the function """
    url = 'http://localhost:5000/sessions'
    response = requests.delete(url=url, cookies={'session_id': session_id})
    assert response.status_code == 200
    assert response.json() == {'message': 'Bienvenue'}


def reset_password_token(email: str) -> str:
    """ Here the function """
    url = 'http://localhost:5000/reset_password'
    data = {'email': email}
    response = requests.post(url=url, data=data)
    if response.status_code == 200:
        content = response.json()
        assert response.status_code == 200
        assert 'reset_token' in list(content.keys())
        return content['reset_token']
    else:
        assert response.status_code == 403
        return None


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ Here the function """
    url = 'http://localhost:5000/reset_password'
    data = {
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password
    }
    response = requests.put(url=url, data=data)
    assert response.status_code == 200
    assert response.json() == {'email': email, 'message': 'Password updated'}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
