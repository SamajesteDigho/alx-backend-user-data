#!/usr/bin/env python3
""" Our user model module as we like it
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer


Base = declarative_base()


class User(Base):
    """ User class defined here """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    session_id = Column(String, nullable=True)
    reset_token = Column(String, nullable=True)

    def __repr__(self):
        """ Return the String representation """
        return "[USER] id={}, email={}".format(self.id, self.email)
