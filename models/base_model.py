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
import models
import uuid
from datetime import datetime


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
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        
        if kwargs:
            for key, value in kwargs.items():
                if key == "__class__":
                    continue
                elif key == "created_at" or key == "updated_at":
                    setattr(self, key, datetime.strptime(value, t_format))
                else:
                    setattr(self, key, value)

        models.storage.new(self)

    def __str__(self):
        """
        Returns a string representation of the instance,
        including its class name, id, and attributes.
        """
        class_name = self.__class__.__name__
        return "[{}] ({}) {}".format(class_name, self.id, self.__dict__)

    def save(self):
        """
        Updates the 'updated_at' to the current datetime.
        """
        self.updated_at = datetime.utcnow()
        models.storage.save()

    def to_dict(self):
        """
        Turns the instance attributes into a dictionary representation
        using 'simple object type'.
        """
        dic_rep  = self.__dict__.copy()
        dic_rep ["__class__"] = self.__class__.__name__
        dic_rep ["created_at"] = self.created_at.isoformat()
        dic_rep ["updated_at"] = self.updated_at.isoformat()

        return dic_rep


if __name__ == "__main__":
    my_model = BaseModel()
    my_model.name = "My_First_Model"
    my_model.my_number = 89
    print(my_model.id)
    print(my_model)
    print(type(my_model.created_at))
    print("--")
    my_model_json = my_model.to_dict()
    print(my_model_json)
    print("JSON of my_model:")
    for key in my_model_json.keys():
        print("\t{}: ({}) - {}".format(key, type(my_model_json[key]), my_model_json[key]))

    print("--")
    my_new_model = BaseModel(**my_model_json)
    print(my_new_model.id)
    print(my_new_model)
    print(type(my_new_model.created_at))

    print("--")
    print(my_model is my_new_model)