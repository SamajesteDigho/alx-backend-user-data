#!/usr/bin/env python3
""" Basic Authentication module
"""
import base64
from typing import Tuple, TypeVar
from api.v1.auth.auth import Auth
from api.v1.views.users import User


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

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """ Decoding the base64 """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            data = base64.b64decode(s=base64_authorization_header)
            return data.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> Tuple[str, str]:
        """ Getting the user credentials """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        data = decoded_base64_authorization_header.split(':', maxsplit=1)
        return data[0], data[1]

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str
                                     ) -> TypeVar('User'):  # type: ignore
        """ Getting the user instance fom here """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        users = User.search(attributes={'email': user_email})
        if users is None or len(users) == 0:
            return None
        if not users[0].is_valid_password(user_pwd):
            return None
        return users[0]

    def current_user(self, request=None) -> TypeVar('User'):  # type: ignore
        """ Here we get the current user """
        auth_header = self.authorization_header(request=request)
        auth_data = self.extract_base64_authorization_header(auth_header)
        dec_data = self.decode_base64_authorization_header(auth_data)
        cred = self.extract_user_credentials(dec_data)
        entity = self.user_object_from_credentials(cred[0], cred[1])
        return entity
