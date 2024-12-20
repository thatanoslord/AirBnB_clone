#!/usr/bin/python3
"""Defines the Place class."""
from models.base_model import BaseModel


class Place(BaseModel):
    """Represents a Place.

    Attributes:
    city_id (str): The ID of the city where the place is located.
    user_id (str): The ID of the user associated with the place.
    name (str): The name of the place.
    description (str): A description of the place.
    number_rooms (int): The total number of rooms in the place.
    number_bathrooms (int): The total number of bathrooms in the place.
    max_guest (int): The maximum capacity of guests for the place.
    price_by_night (int): The cost per night for staying at the place
    latitude (float): The geographical latitude of the place.
    longitude (float): The geographical longitude of the place.
    amenity_ids (list): A list of IDs representing the amenities
    available at the place."""

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
