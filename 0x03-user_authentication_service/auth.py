#!/usr/bin/env python3
""" Our Auth module as we like it
"""
from typing import Union
import bcrypt
from sqlalchemy.exc import NoResultFound
from uuid import uuid4
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """ Here we hash the password """
    salt = bcrypt.gensalt()
    by_pass = password.encode('utf-8')
    return bcrypt.hashpw(password=by_pass, salt=salt)


def _generate_uuid() -> str:
    """ Generating the UUID """
    return str(uuid4())


class Auth:
    """ Authentication class definition """
    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Registering a user """
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError("User {} already exist".format(email))
        except NoResultFound:
            hpass = _hash_password(password=password)
            user = self._db.add_user(email=email, hashed_password=hpass)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """ Validating password """
        try:
            user = self._db.find_user_by(email=email)
            crp_pass = password.encode('utf-8')
            if bcrypt.checkpw(crp_pass, user.hashed_password):
                return True
            else:
                return False
        except Exception:
            return False

    def create_session(self, email: str) -> str:
        """ Creating a new session """
        try:
            user = self._db.find_user_by(email=email)
            user.session_id = _generate_uuid()
            self._db._session.commit()
            return user.session_id
        except Exception:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """ Using session id to get user """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except Exception:
            return None

    def destroy_session(self, user_id: int) -> None:
        """ Destroying the user session """
        if user_id is None:
            return None
        try:
            user = self._db.find_user_by(id=user_id)
            user.session_id = None
            self._db._session.commit()
            return None
        except Exception:
            return None

    def get_reset_password_token(self, email) -> str:
        """ Initiating password reset token """
        try:
            user = self._db.find_user_by(email=email)
            user.reset_token = _generate_uuid()
            self._db._session.commit()
            return user.reset_token
        except Exception:
            raise ValueError('User does not exist')

    def update_password(self, reset_token: str, password: str) -> None:
        """ Updating user password """
        try:
            user = self._db.find_user_by(reset_token)
            user.hashed_password = _hash_password(password=password)
            user.reset_token = None
            self._db._session.commit()
        except Exception:
            raise ValueError('Reset token not found')