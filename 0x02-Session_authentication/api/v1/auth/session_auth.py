#!/usr/bin/env python3
""" Basic Authentication module
"""
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
