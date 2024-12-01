#!/usr/bin/env python3
"""
Unit Test Module for Amenity Class
"""
import unittest
from models.amenity import Amenity
from models.base_model import BaseModel
import models
import os


class TestAmenity(unittest.TestCase):
    """Test cases for the Amenity class"""

    def setUp(self):
        """Set up test methods"""
        self.amenity = Amenity()

    def tearDown(self):
        """Clean up after test methods"""
        try:
            os.remove("file.json")
        except:
            pass

    def test_amenity_inheritance(self):
        """Test if Amenity inherits from BaseModel"""
        self.assertIsInstance(self.amenity, BaseModel)
        self.assertTrue(hasattr(self.amenity, "id"))
        self.assertTrue(hasattr(self.amenity, "created_at"))
        self.assertTrue(hasattr(self.amenity, "updated_at"))

    def test_amenity_attributes(self):
        """Test Amenity class attributes"""
        self.assertTrue(hasattr(self.amenity, "name"))
        self.assertEqual(self.amenity.name, "")

    def test_amenity_attribute_assignment(self):
        """Test attribute assignment"""
        test_name = "WiFi"
        self.amenity.name = test_name
        self.assertEqual(self.amenity.name, test_name)

    def test_to_dict_method(self):
        """Test to_dict method"""
        self.amenity.name = "Pool"
        amenity_dict = self.amenity.to_dict()

        self.assertIsInstance(amenity_dict, dict)
        self.assertEqual(amenity_dict['__class__'], 'Amenity')
        self.assertEqual(amenity_dict['name'], "Pool")
        self.assertIsInstance(amenity_dict['created_at'], str)
        self.assertIsInstance(amenity_dict['updated_at'], str)
