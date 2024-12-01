#!/usr/bin/env python3
"""
Unit Test Module for User Class
This module contains test cases for the User class
"""
import unittest
from models.user import User
from models.base_model import BaseModel
from datetime import datetime
import models
import os


class TestUser(unittest.TestCase):
    """Test cases for the User class"""

    def setUp(self):
        """Set up test methods"""
        self.user = User()
        self.test_email = "test@test.com"
        self.test_password = "testpass123"
        self.test_first_name = "John"
        self.test_last_name = "Doe"

    def tearDown(self):
        """Clean up after test methods"""
        try:
            os.remove("file.json")
        except:
            pass

    def test_user_inheritance(self):
        """Test if User inherits from BaseModel"""
        self.assertIsInstance(self.user, BaseModel)
        self.assertTrue(hasattr(self.user, "id"))
        self.assertTrue(hasattr(self.user, "created_at"))
        self.assertTrue(hasattr(self.user, "updated_at"))

    def test_user_attributes(self):
        """Test User class attributes"""
        # Check if all required attributes exist
        self.assertTrue(hasattr(self.user, "email"))
        self.assertTrue(hasattr(self.user, "password"))
        self.assertTrue(hasattr(self.user, "first_name"))
        self.assertTrue(hasattr(self.user, "last_name"))

        # Check default values
        self.assertEqual(self.user.email, "")
        self.assertEqual(self.user.password, "")
        self.assertEqual(self.user.first_name, "")
        self.assertEqual(self.user.last_name, "")

    def test_user_attribute_assignment(self):
        """Test attribute assignment for User class"""
        self.user.email = self.test_email
        self.user.password = self.test_password
        self.user.first_name = self.test_first_name
        self.user.last_name = self.test_last_name

        self.assertEqual(self.user.email, self.test_email)
        self.assertEqual(self.user.password, self.test_password)
        self.assertEqual(self.user.first_name, self.test_first_name)
        self.assertEqual(self.user.last_name, self.test_last_name)

    def test_to_dict_method(self):
        """Test to_dict method of User class"""
        self.user.email = self.test_email
        self.user.password = self.test_password
        user_dict = self.user.to_dict()

        self.assertIsInstance(user_dict, dict)
        self.assertEqual(user_dict['__class__'], 'User')
        self.assertEqual(user_dict['email'], self.test_email)
        self.assertEqual(user_dict['password'], self.test_password)
        self.assertIsInstance(user_dict['created_at'], str)
        self.assertIsInstance(user_dict['updated_at'], str)

    def test_str_representation(self):
        """Test string representation of User instance"""
        string = str(self.user)
        self.assertIn("[User]", string)
        self.assertIn("id", string)
        self.assertIn("created_at", string)
        self.assertIn("updated_at", string)

    def test_save_method(self):
        """Test save method of User class"""
        old_updated_at = self.user.updated_at
        self.user.save()
        self.assertNotEqual(old_updated_at, self.user.updated_at)
        self.assertTrue(os.path.exists("file.json"))

    def test_create_user_from_dictionary(self):
        """Test creating a User instance from dictionary"""
        self.user.email = self.test_email
        self.user.password = self.test_password
        user_dict = self.user.to_dict()
        new_user = User(**user_dict)

        self.assertEqual(new_user.email, self.user.email)
        self.assertEqual(new_user.password, self.user.password)
        self.assertEqual(new_user.id, self.user.id)
        self.assertEqual(new_user.created_at, self.user.created_at)
        self.assertEqual(new_user.updated_at, self.user.updated_at)
        self.assertIsNot(new_user, self.user)

    def test_invalid_attribute_assignment(self):
        """Test assignment of invalid attributes"""
        with self.assertRaises(AttributeError):
            self.user.__created_at = datetime.now()
        with self.assertRaises(AttributeError):
            self.user.__updated_at = datetime.now()
        with self.assertRaises(AttributeError):
            self.user.__id = "invalid_id"

    def test_user_storage(self):
        """Test if User instance is properly stored"""
        self.user.save()
        all_objects = models.storage.all()
        self.assertIn(f"User.{self.user.id}", all_objects.keys())
        self.assertEqual(all_objects[f"User.{self.user.id}"], self.user)


if __name__ == '__main__':
    unittest.main()
