#!/usr/bin/env python3
""" Basic Authentication module
"""
from .auth import Auth


class BasicAuth(Auth):
    """ Class for defining basic authentiation """

    def __init__(self) -> None:
        """ Here the initialization """
        super().__init__()

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ Extraction base64 """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]
