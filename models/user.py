#!/usr/bin/python3
"""This is the user class"""
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from models.place import Place
from models.review import Review
from sqlalchemy.ext.declarative import declarative_base


class User(BaseModel, Base):
    """This class defines a user by various attributes"""
    __tablename__ = 'users'

    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)

    places = relationship("Place", backref="user",
                          cascade="all, delete-orphan")
    reviews = relationship("Review", cascade="all, delete,
                           delete-orphan", backref="user")
