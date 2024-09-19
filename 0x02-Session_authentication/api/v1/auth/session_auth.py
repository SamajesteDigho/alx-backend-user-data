#!/usr/bin/env python3
""" Basic Authentication module
"""
import os
from api.v1.auth.auth import Auth
from uuid import uuid4


class SessionAuth(Auth):
    """ Session Auth class """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Creating a session """
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        key = str(uuid4())
        self.user_id_by_session_id[key] = user_id
        return key

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ User id session """
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def session_cookie(self, request=None):
        """ Preparing session cookies """
        if request is None:
            return None
        cookie_name = os.getenv('SESSION_NAME', None)
        if cookie_name is None:
            return None
        return request.cookies.get(cookie_name, None)
