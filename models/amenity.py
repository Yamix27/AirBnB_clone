#!/usr/bin/python3
"""
Module: amenity.py

Defines the Amenity class, a subclass of BaseModel.

The Amenity class represents an amenity associated
with a place in the AirBnB clone project.
"""

from models.base_model import BaseModel


class Amenity(BaseModel):
    """
    Amenity class for representing amenities
    in the AirBnB clone project.

    Attributes:
        name (str): Amenity name.
    """
    name = ""
