#!/usr/bin/env python3
"""
Unit Test Module for State Class
"""
import unittest
from models.state import State
from models.base_model import BaseModel
import models
import os


class TestState(unittest.TestCase):
    """Test cases for the State class"""

    def setUp(self):
        """Set up test methods"""
        self.state = State()

    def tearDown(self):
        """Clean up after test methods"""
        try:
            os.remove("file.json")
        except:
            pass

    def test_state_inheritance(self):
        """Test if State inherits from BaseModel"""
        self.assertIsInstance(self.state, BaseModel)
        self.assertTrue(hasattr(self.state, "id"))
        self.assertTrue(hasattr(self.state, "created_at"))
        self.assertTrue(hasattr(self.state, "updated_at"))

    def test_state_attributes(self):
        """Test State class attributes"""
        self.assertTrue(hasattr(self.state, "name"))
        self.assertEqual(self.state.name, "")

    def test_state_attribute_assignment(self):
        """Test attribute assignment"""
        test_name = "California"
        self.state.name = test_name
        self.assertEqual(self.state.name, test_name)

    def test_to_dict_method(self):
        """Test to_dict method"""
        self.state.name = "Texas"
        state_dict = self.state.to_dict()

        self.assertIsInstance(state_dict, dict)
        self.assertEqual(state_dict['__class__'], 'State')
        self.assertEqual(state_dict['name'], "Texas")
        self.assertIsInstance(state_dict['created_at'], str)
        self.assertIsInstance(state_dict['updated_at'], str)

    def test_str_representation(self):
        """Test string representation"""
        string = str(self.state)
        self.assertIn("[State]", string)
        self.assertIn("id", string)

    def test_state_save(self):
        """Test save method"""
        self.state.name = "New York"
        old_updated_at = self.state.updated_at
        self.state.save()
        self.assertNotEqual(old_updated_at, self.state.updated_at)
