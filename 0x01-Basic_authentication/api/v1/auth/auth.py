#!/usr/bin/env python3
""" Module of Auth class
"""
from typing import List, TypeVar
from flask import request


class Auth:
    """ Here the Auth class for managing authentications """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Requiring authentication """
        return False

    def authorization_header(self, request=None) -> str:
        """ Authorization Header """
        return None

    def current_user(self, request=None) -> TypeVar('User'):  # type: ignore
        """ Getting the current user """
        return None
