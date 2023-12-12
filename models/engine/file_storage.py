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
        return FileStorage.__objects

    def new(self, obj):
        """
        Adds a new instance to the storage.

        Args:
            obj (BaseModel): The Added object into storage.
        """
        obj_class_name = obj.__class__.__name__
        key = "{}.{}".format(obj_class_name, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """
        Serializes stored instance to the JSON file.
        """
        objs = FileStorage.__objects
        obj_dict = {}

        for obj in objs.keys():
            obj_dict[obj] = objs[obj].to_dict()

        with open(FileStorage.__file_path, "w", encoding="utf-8") as file:
            json.dump(obj_dict, file)

    def reload(self):
        """
        Deserializes the JSON file to the stored instance.
        """
        if os.path.isfile(FileStorage.__file_path):
            with open(FileStorage.__file_path, "r", encoding="utf-8") as file:
                try:
                    obj_dict = json.load(file)

                    for key, value in obj_dict.items():
                        class_name, obj_id = key.split('.')

                        cls = eval(class_name)

                        instance = cls(**value)

                        FileStorage.__objects[key] = instance
                except Exception:
                    pass
