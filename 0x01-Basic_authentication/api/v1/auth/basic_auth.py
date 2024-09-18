#!/usr/bin/env python3
""" Basic Authentication module
"""
from .auth import Auth


class BasicAuth(Auth):
    """ Class for defining basic authentiation """

    def __init__(self) -> None:
        """ Here the initialization """
        super().__init__()
