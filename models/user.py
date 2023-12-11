#!/usr/bin/python3
"""
Module: user.py

Defines the User class, a subclass of BaseModel.

The User class represents users
in the AirBnB clone project.
"""

from models.base_model import BaseModel


class User(BaseModel):
    """
    User class for representing users
    in the AirBnB clone project.

    Attributes:
        email (str): Email address of the user.
        password (str): Password associated with the user.
        first_name (str): First name of the user.
        last_name (str): Last name of the user.
    """
    email = ""
    password = ""
    first_name = ""
    last_name = ""