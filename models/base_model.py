#!/usr/bin/python3
"""
Module: base_model.py

Defines the BaseModel class, the parent class for all
other classes in the AirBnB clone project.
Handles instance initialization, serialization
and deserialization.

Classes:
- BaseModel: The base class for objects
in the AirBnB clone project.

Attributes:
- id (str): Unique identifier generated for each instance.
- created_at (datetime): Instance creation time.
- updated_at (datetime): Instance last update time.

Methods:
- __init__(self, *args, **kwargs): BaseModel constructor.
- __str__(self): Returns a string representation of the instance.
- save(self): Updates the instance's updated_at attribute and saves.
- to_dict(self): Returns a dictionary instance for serialization.

Usage:
from models.base_model import BaseModel

# Instantiate BaseModel
base_model = BaseModel()

# Perform operations on the instance
base_model.save()  # Persist changes to JSON file
base_model_dict = base_model.to_dict()
"""

from datetime import datetime
import models
import uuid


class BaseModel:
    """
    BaseModel class defines common attributes/methods for other classes.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor for the BaseModel class.
        Initializes instance attributes based on provided keyword
        arguments or generates default values for id, created_at,
        and updated_at.
        """
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            self.created_at = datetime.strptime(self.created_at, t_format)
            self.updated_at = datetime.strptime(self.updated_at, t_format)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at
        models.storage.new(self)

    def __str__(self):
        """
        Returns a string representation of the instance,
        including its class name, id, and attributes.
        """
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """
        Updates the 'updated_at' to the current datetime.
        """
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """
        Turns the instance attributes into a dictionary representation
        using 'simple object type'.
        """

        dic_rep = {}
        dic_rep["__class__"] = self.__class__.__name__

        for key, value in self.__dict__.items():
            if isinstance(value, datetime):
                dic_rep[key] = value.isoformat()
            else:
                dic_rep[key] = value
        return dic_rep
