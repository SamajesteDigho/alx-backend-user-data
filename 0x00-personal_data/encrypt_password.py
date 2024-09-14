#!/usr/bin/env python3
"""
Here the module description
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """ Crypting the password """
    salt = bcrypt.gensalt()
    psw = bytes(password, 'utf-8')
    return bcrypt.hashpw(password=psw, salt=salt)
