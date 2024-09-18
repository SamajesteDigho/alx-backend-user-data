#!/usr/bin/env python3
""" Module of Auth class
"""
from typing import List, TypeVar
from flask import request


class Auth:
    """ Here the Auth class for managing authentications """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Requiring authentication """
        if path is None or excluded_paths is None:
            return True
        dupplit = path
        if path[-1] == '/':
            dupplit = path[:-1]
        else:
            dupplit = "{}/".format(path)
        if path in excluded_paths or dupplit in excluded_paths:
            return False
        for x in excluded_paths:
            if path.startswith(x[:-1]):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Authorization Header """
        if request is None:
            return None
        if "Authorization" not in list(request.headers.keys()):
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):  # type: ignore
        """ Getting the current user """
        return None
