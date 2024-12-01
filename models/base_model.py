#!/usr/bin/python3
"""defines all common attributes/methods for other classes:
    """

import datetime
import uuid
import models


class BaseModel:
    """defines all common attributes/methods for other classes:
    """

    def __init__(self, *args, **kwargs) -> None:
        """Initialization of Public instance attributes
        """
        if kwargs != {} and kwargs is not None:
            for key, value in kwargs.items():
                if key != '__class__':
                    if key == 'created_at' or key == 'updated_at':
                        self.__dict__[key] = datetime.datetime.strptime(
                            kwargs[key], "%Y-%m-%dT%H:%M:%S.%f")
                    else:
                        self.__dict__[key] = value
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.datetime.now()
            self.updated_at = datetime.datetime.now()
            models.storage.new(self)

    def __str__(self) -> str:
        """print: [<class name>] (<self.id>) <self.__dict__>

        Returns:
            str: string representation
        """
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """updates the public instance attribute updated_at with the
        current datetime
        """
        # try:
        self.updated_at = datetime.datetime.now()
        # d1 = self.to_dict()
        # print(d1)
        models.storage.new(self)
        models.storage.save()
        # except PermissionError:
        #     raise PermissionError("You don't have write permission")

    def to_dict(self):
        """returns a dictionary containing all keys/values of the instance

        Returns:
                dict: all keys/values of the instance
        """
        d1 = dict(self.__dict__)  # Cloning d1 from self.__dict__
        # print(f"d1 is self.__dict__: {d1 is self.__dict__}")
        d1["__class__"] = self.__class__.__name__
        # created_at and updated_at must be converted to string object in ISO
        # format isoformat()
        d1['updated_at'] = d1['updated_at'].isoformat()
        if type(d1['created_at']) is not str:
            d1['created_at'] = d1['created_at'].isoformat()
        return d1
