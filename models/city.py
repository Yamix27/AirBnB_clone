#!/usr/bin/python3
"""
Module: city.py

Defines the City class, a subclass of BaseModel.

The City class represents a city
in the AirBnB clone project.
"""

from models.base_model import BaseModel


class City(BaseModel):
    """
    City class for representing cities
    in the AirBnB clone project.

    Attributes:
        state_id (str): ID of the State.
        name (str): Name of the city.
    """
    state_id = ""
    name = ""
