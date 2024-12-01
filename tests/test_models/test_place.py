#!/usr/bin/env python3
"""
Unit Test Module for Place Class
"""
import unittest
from models.place import Place
from models.base_model import BaseModel
import models
import os


class TestPlace(unittest.TestCase):
    """Test cases for the Place class"""

    def setUp(self):
        """Set up test methods"""
        self.place = Place()

    def tearDown(self):
        """Clean up after test methods"""
        try:
            os.remove("file.json")
        except:
            pass

    def test_place_inheritance(self):
        """Test if Place inherits from BaseModel"""
        self.assertIsInstance(self.place, BaseModel)
        self.assertTrue(hasattr(self.place, "id"))
        self.assertTrue(hasattr(self.place, "created_at"))
        self.assertTrue(hasattr(self.place, "updated_at"))

    def test_place_attributes(self):
        """Test Place class attributes"""
        # Test for attribute existence and default values
        attributes = {
            "city_id": "",
            "user_id": "",
            "name": "",
            "description": "",
            "number_rooms": 0,
            "number_bathrooms": 0,
            "max_guest": 0,
            "price_by_night": 0,
            "latitude": 0.0,
            "longitude": 0.0,
            "amenity_ids": []
        }

        for attr, default in attributes.items():
            self.assertTrue(hasattr(self.place, attr))
            self.assertEqual(getattr(self.place, attr), default)

    def test_place_attribute_types(self):
        """Test Place attribute types"""
        self.assertIsInstance(self.place.city_id, str)
        self.assertIsInstance(self.place.user_id, str)
        self.assertIsInstance(self.place.name, str)
        self.assertIsInstance(self.place.description, str)
        self.assertIsInstance(self.place.number_rooms, int)
        self.assertIsInstance(self.place.number_bathrooms, int)
        self.assertIsInstance(self.place.max_guest, int)
        self.assertIsInstance(self.place.price_by_night, int)
        self.assertIsInstance(self.place.latitude, float)
        self.assertIsInstance(self.place.longitude, float)
        self.assertIsInstance(self.place.amenity_ids, list)

    def test_place_attribute_assignment(self):
        """Test attribute assignment"""
        self.place.city_id = "city-123"
        self.place.user_id = "user-123"
        self.place.name = "Cozy Cottage"
        self.place.description = "A beautiful cottage"
        self.place.number_rooms = 2
        self.place.number_bathrooms = 1
        self.place.max_guest = 4
        self.place.price_by_night = 100
        self.place.latitude = 37.7749
        self.place.longitude = -122.4194
        self.place.amenity_ids = ["amenity-1", "amenity-2"]

        self.assertEqual(self.place.city_id, "city-123")
        self.assertEqual(self.place.user_id, "user-123")
        self.assertEqual(self.place.name, "Cozy Cottage")
        self.assertEqual(self.place.description, "A beautiful cottage")
        self.assertEqual(self.place.number_rooms, 2)
        self.assertEqual(self.place.number_bathrooms, 1)
        self.assertEqual(self.place.max_guest, 4)
        self.assertEqual(self.place.price_by_night, 100)
        self.assertEqual(self.place.latitude, 37.7749)
        self.assertEqual(self.place.longitude, -122.4194)
        self.assertEqual(self.place.amenity_ids, ["amenity-1", "amenity-2"])

    def test_to_dict_method(self):
        """Test to_dict method"""
        self.place.city_id = "city-123"
        self.place.name = "Beach House"
        place_dict = self.place.to_dict()

        self.assertIsInstance(place_dict, dict)
        self.assertEqual(place_dict['__class__'], 'Place')
        self.assertEqual(place_dict['city_id'], "city-123")
        self.assertEqual(place_dict['name'], "Beach House")
        self.assertIsInstance(place_dict['created_at'], str)
        self.assertIsInstance(place_dict['updated_at'], str)

    def test_numeric_values(self):
        """Test numeric value constraints"""
        # Test negative values
        self.place.number_rooms = -1
        self.place.number_bathrooms = -1
        self.place.max_guest = -1
        self.place.price_by_night = -1

        # These should either raise an exception or be constrained to 0
        # depending on your implementation
        self.assertGreaterEqual(self.place.number_rooms, 0)
        self.assertGreaterEqual(self.place.number_bathrooms, 0)
        self.assertGreaterEqual(self.place.max_guest, 0)
        self.assertGreaterEqual(self.place.price_by_night, 0)
