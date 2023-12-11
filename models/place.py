#!/usr/bin/python3
"""
Module: place.py

Defines the Place class, a subclass of BaseModel.

The Place class represents a place available for rent
in the AirBnB clone project.
"""

from models.base_model import BaseModel


class Place(BaseModel):
    """
    Place class for representing rental places
    in the AirBnB clone project.

    Attributes:
        city_id (str): ID of the city location of the place.
        user_id (str): ID of the owner of the place.
        name (str): Name of the place.
        description (str): Description of the place.
        number_rooms (int): Number of rooms in the place.
        number_bathrooms (int): Number of bathrooms in the place.
        max_guest (int): Maximum number of guests allowed.
        price_by_night (int): Price per night for renting the place.
        latitude (float): Latitude coordinate of the place.
        longitude (float): Longitude coordinate of the place.
        amenity_ids (list): List of the place amenity IDs.
    """

    city_id = ""
    user_id = ""
    name = ""
    description = ""
    number_rooms = 0
    number_bathrooms = 0
    max_guest = 0
    price_by_night = 0
    latitude = 0.0
    longitude = 0.0
    amenity_ids = []
