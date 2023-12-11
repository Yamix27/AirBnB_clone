#!/usr/bin/python3
"""
Module: file_storage.py

Manages the serialization and deserialization
of objects to and from JSON files.

Class:
- FileStorage: Handles storage and retrieval
of instances to/from JSON files.

Attributes:
- __file_path (str): Path to the JSON file.
- __objects (dict): Dictionary to store instances
by their class name and ID.

Methods:
- all(self): Returns the dictionary of stored objects.
- new(self, obj): Adds an object to the storage.
- save(self): Serializes the objects and saves to the JSON file.
- reload(self): Deserializes the JSON file and loads objects.

Usage:
from models.engine.file_storage import FileStorage

# Instantiate FileStorage
storage = FileStorage()

# Load existing object data from the JSON file
storage.reload()

# Perform operations on instances (create, update, delete)
# Call storage.save() after each operation to persist changes
"""

import json
import os

from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.review import Review
from models.state import State
from models.city import City
from models.place import Place


class FileStorage:
    """
    Manages the serialization and deserialization
    of objects to and from JSON files.
    """

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """
        Returns the stored objects in a dictionary.

        Returns:
            dict: A dictionary containing all stored objects.
        """
        return self.__objects

    def new(self, obj):
        """
        Adds a new instance to the storage.

        Args:
            obj (BaseModel): The Added object into storage.
        """
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.__objects[key] = obj

    def save(self):
        """
        Serializes stored instance to the JSON file.
        """
        with open(FileStorage.__file_path, 'w+') as f:
            res = {}
            for key, value in FileStorage.__objects.items():
                res[key] = value.to_dict()
            json.dump(res, f)

    def reload(self):
        """
        Deserializes the JSON file to the stored instance.
        """
        try:
            with open(FileStorage.__file_path, 'r') as f:
                dictofobjs = json.loads(f.read())
                from models.base_model import BaseModel
                from models.user import User
                for key, value in dictofobjs.items():
                    if value['__class__'] == 'BaseModel':
                        FileStorage.__objects[key] = BaseModel(**value)
                    elif value['__class__'] == 'User':
                        FileStorage.__objects[key] = User(**value)
                    elif value['__class__'] == 'Place':
                        FileStorage.__objects[key] = Place(**value)
                    elif value['__class__'] == 'State':
                        FileStorage.__objects[key] = State(**value)
                    elif value['__class__'] == 'City':
                        FileStorage.__objects[key] = City(**value)
                    elif value['__class__'] == 'Amenity':
                        FileStorage.__objects[key] = Amenity(**value)
                    elif value['__class__'] == 'Review':
                        FileStorage.__objects[key] = Review(**value)

        except FileNotFoundError:
            pass
