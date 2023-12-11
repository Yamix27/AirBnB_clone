#!/usr/bin/python3
"""
Module: state.py

Defines the State class, a subclass of BaseModel.

The State class represents states
in the AirBnB clone project.
"""

from models.base_model import BaseModel


class State(BaseModel):
    """
    State class for representing states
    in the AirBnB clone project.

    Attributes:
        name (str): Name of the state.
    """
    name = ""
