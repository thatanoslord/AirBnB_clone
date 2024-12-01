#!/usr/bin/env python3
"""
Unit Test Module for City Class
"""
import unittest
from models.city import City
from models.base_model import BaseModel
import models
import os


class TestCity(unittest.TestCase):
    """Test cases for the City class"""

    def setUp(self):
        """Set up test methods"""
        self.city = City()

    def tearDown(self):
        """Clean up after test methods"""
        try:
            os.remove("file.json")
        except:
            pass

    def test_city_inheritance(self):
        """Test if City inherits from BaseModel"""
        self.assertIsInstance(self.city, BaseModel)
        self.assertTrue(hasattr(self.city, "id"))
        self.assertTrue(hasattr(self.city, "created_at"))
        self.assertTrue(hasattr(self.city, "updated_at"))

    def test_city_attributes(self):
        """Test City class attributes"""
        self.assertTrue(hasattr(self.city, "state_id"))
        self.assertTrue(hasattr(self.city, "name"))
        self.assertEqual(self.city.state_id, "")
        self.assertEqual(self.city.name, "")

    def test_city_attribute_assignment(self):
        """Test attribute assignment"""
        test_state_id = "test-state-id"
        test_name = "San Francisco"
        self.city.state_id = test_state_id
        self.city.name = test_name
        self.assertEqual(self.city.state_id, test_state_id)
        self.assertEqual(self.city.name, test_name)

    def test_to_dict_method(self):
        """Test to_dict method"""
        self.city.state_id = "CA-01"
        self.city.name = "Los Angeles"
        city_dict = self.city.to_dict()

        self.assertIsInstance(city_dict, dict)
        self.assertEqual(city_dict['__class__'], 'City')
        self.assertEqual(city_dict['state_id'], "CA-01")
        self.assertEqual(city_dict['name'], "Los Angeles")
        self.assertIsInstance(city_dict['created_at'], str)
        self.assertIsInstance(city_dict['updated_at'], str)
