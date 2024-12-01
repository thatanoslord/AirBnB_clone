#!/usr/bin/python3
"""serializes instances to a JSON file and deserializes JSON file to instances:

    """
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from os.path import isfile


class FileStorage:
    """Represent an abstracted storage engine.

    Attributes:
        __file_path (str): The name of the file to save objects to.
        __objects (dict): A dictionary of instantiated objects.
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """returns the dictionary __objects

        Returns:
            dict: _description_
        """
        return FileStorage.__objects

    def new(self, obj):
        """ sets in __objects the obj with key <obj class name>.id

        Args:
            obj (BaseModel): _description_
        """
        # print("tst")
        # print(obj.id)
        # print(f"{obj.__class__.__name__}")
        # print(obj)
        FileStorage.__objects[f"{obj.__class__.__name__}.{obj.id}"] = obj
        # print(self.__objects)

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)
        """
        d1 = dict()
        for obj_id in FileStorage.__objects.keys():
            d1[obj_id] = FileStorage.__objects[obj_id].to_dict()
        with open(FileStorage.__file_path, mode="w") as file:
            json.dump(d1, file)

    def reload(self):
        """deserializes the JSON file to __objects (only if the JSON file
        (__file_path) exists ; otherwise, do nothing. If the
        file doesn’t exist, no exception should be raised)
        """
        # print(isfile(self.__file_path))
        if isfile(self.__file_path):
            with open(FileStorage.__file_path) as f:
                objdict = json.load(f)
                for o in objdict.values():
                    cls_name = o["__class__"]
                    del o["__class__"]
                    self.new(eval(cls_name)(**o))
