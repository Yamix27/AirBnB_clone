#!/usr/bin/python3
"""
Module: review.py

Defines the Review class, a subclass of BaseModel.

The Review class represents reviews of places in
the AirBnB clone project.
"""

from models.base_model import BaseModel


class Review(BaseModel):
    """
    Review class for representing reviews of places
    in the AirBnB clone project.

    Attributes:
        place_id (str): ID of the place being reviewed.
        user_id (str): ID of the review writer.
        text (str): The review text.
    """
    place_id = ""
    user_id = ""
    text = ""
