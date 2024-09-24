#!/usr/bin/env python3
""" Our DB module as we like it
"""
from typing import TypeVar
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import NoResultFound, InvalidRequestError

from user import Base, User


class DB:
    """ DB class
    """

    def __init__(self) -> None:
        """ Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """ Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ Adding a user to the DB """
        try:
            user = User(email=email, hashed_password=hashed_password)
            self._session.add(user)
            self._session.commit()
            return user
        except Exception:
            return None

    def find_user_by(self, **kwargs) -> User:
        """ Finding a user from the DB """
        if kwargs is not None:
            try:
                query = self._session.query(User)
                for key, val in kwargs.items():
                    query = query.filter(getattr(User, key) == val)
                user = query.first()
                if user is None:
                    raise NoResultFound
                return user
            except NoResultFound:
                raise NoResultFound
            except AttributeError:
                raise InvalidRequestError

    def update_user(self, user_id: int, **kwargs):
        """ Let's update the user now """
        try:
            user = self.find_user_by(id=user_id)
            for key, value in kwargs.items():
                user.__setattr__(key, value)
            self._session.commit()
        except InvalidRequestError:
            raise ValueError
