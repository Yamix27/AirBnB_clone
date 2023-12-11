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
        if os.path.exists(self.__file_path):
            try:
                with open(self.__file_path, "r",
                          encoding="utf-8") as data_file:
                    json_data = json.load(data_file)
                    for key, value in json_data.items():
                        if '.' in key:
                            class_name, obj_id = key.split('.')
                            class_obj = globals()[class_name]
                            new_instance = class_obj(**value)
                            self.new(new_instance)
                            self.__objects[key] = new_instance
            except FileNotFoundError:
                pass
