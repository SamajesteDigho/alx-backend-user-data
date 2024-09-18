#!/usr/bin/env python3
""" Module of Auth class
"""
from typing import List, TypeVar
from flask import request


class Auth:
    """ Here the Auth class for managing authentications """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Requiring authentication """
        if path is None  or excluded_paths is None:
            return True
        new = None
        if path[-1] == '/':
            new = f"{path[:-1]}"
        else:
            new = f"{path}/"
        if path in excluded_paths or new in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Authorization Header """
        return None

    def current_user(self, request=None) -> TypeVar('User'):  # type: ignore
        """ Getting the current user """
        return None
