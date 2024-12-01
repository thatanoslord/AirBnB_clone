#!/usr/bin/python3
"""
Comprehensive unit tests for BaseModel class.
Tests all possible edge cases and scenarios.
"""
from console import HBNBCommand
from io import StringIO
from unittest.mock import patch
from models.engine.file_storage import FileStorage
import unittest
from datetime import datetime
from models.base_model import BaseModel
from models import storage
from time import sleep
import os
import json
import uuid
import copy


class TestBaseModel(unittest.TestCase):
    """
    Test cases for BaseModel class.
    Tests initialization, methods, and edge cases.
    """

    def setUp(self):
        """Set up test environment before each test"""
        try:
            os.remove("file.json")
        except:
            pass
        self.base = BaseModel()

    def tearDown(self):
        """Clean up test environment after each test"""
        try:
            os.remove("file.json")
        except:
            pass

    def test_init_no_args(self):
        """Test initialization without arguments"""
        self.assertIsInstance(self.base, BaseModel)
        self.assertTrue(hasattr(self.base, 'id'))
        self.assertTrue(hasattr(self.base, 'created_at'))
        self.assertTrue(hasattr(self.base, 'updated_at'))
        self.assertIsInstance(self.base.id, str)
        self.assertIsInstance(self.base.created_at, datetime)
        self.assertIsInstance(self.base.updated_at, datetime)

    def test_init_with_valid_kwargs(self):
        """Test initialization with valid keyword arguments"""
        date = datetime.now()
        date_iso = date.isoformat()
        kwargs = {
            'id': str(uuid.uuid4()),
            'created_at': date_iso,
            'updated_at': date_iso,
            'name': 'Test Model',
            'number': 89
        }
        model = BaseModel(**kwargs)

        self.assertEqual(model.id, kwargs['id'])
        self.assertEqual(model.created_at.isoformat(), kwargs['created_at'])
        self.assertEqual(model.updated_at.isoformat(), kwargs['updated_at'])
        self.assertEqual(model.name, kwargs['name'])
        self.assertEqual(model.number, kwargs['number'])

    def test_init_with_invalid_kwargs(self):
        """Test initialization with invalid keyword arguments"""
        kwargs = {
            'created_at': 'invalid_date',
            'updated_at': 'invalid_date'
        }
        with self.assertRaises(ValueError):
            BaseModel(**kwargs)

    def test_init_with_args(self):
        """Test initialization with arguments (should be ignored)"""
        model = BaseModel("Ignored", "Args", ["list"], {"dict": "value"})
        self.assertIsInstance(model, BaseModel)
        self.assertTrue(hasattr(model, 'id'))

    def test_init_with_None_kwargs(self):
        """Test initialization with None values in kwargs"""
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)

    def test_str_representation(self):
        """Test string representation of the model"""
        string = str(self.base)
        self.assertIn("[BaseModel]", string)
        self.assertIn(self.base.id, string)
        self.assertIn(str(self.base.__dict__), string)

    def test_to_dict_basic(self):
        """Test basic to_dict functionality"""
        base_dict = self.base.to_dict()
        self.assertIsInstance(base_dict, dict)
        self.assertEqual(base_dict['__class__'], 'BaseModel')
        self.assertIsInstance(base_dict['created_at'], str)
        self.assertIsInstance(base_dict['updated_at'], str)
        self.assertEqual(base_dict['id'], self.base.id)

    def test_to_dict_with_additional_attrs(self):
        """Test to_dict with additional attributes"""
        self.base.name = "Test Model"
        self.base.number = 89
        base_dict = self.base.to_dict()
        self.assertEqual(base_dict['name'], "Test Model")
        self.assertEqual(base_dict['number'], 89)

    def test_to_dict_datetime_format(self):
        """Test datetime format in to_dict"""
        base_dict = self.base.to_dict()
        created_at = datetime.strptime(base_dict['created_at'],
                                       '%Y-%m-%dT%H:%M:%S.%f')
        updated_at = datetime.strptime(base_dict['updated_at'],
                                       '%Y-%m-%dT%H:%M:%S.%f')
        self.assertEqual(created_at, self.base.created_at)
        self.assertEqual(updated_at, self.base.updated_at)

    def test_save_method(self):
        """Test save method functionality"""
        old_updated_at = copy.copy(self.base.updated_at)
        sleep(0.1)  # Ensure time difference
        self.base.save()
        self.assertNotEqual(old_updated_at, self.base.updated_at)

        # Check if saved to file
        key = f"BaseModel.{self.base.id}"
        with open("file.json", "r") as f:
            saved_data = json.load(f)
            self.assertIn(key, saved_data)
            self.assertEqual(saved_data[key]['id'], self.base.id)

    # def test_save_without_permission(self):
    #     """Test save method when file is not writable"""
    #     self.base.save()  # Create the file first
    #     os.chmod("file.json", 0o444)  # Make file read-only
    #     with self.assertRaises(PermissionError):
    #         self.base.save()
    #     os.chmod("file.json", 0o666)  # Restore permissions

    def test_unique_id(self):
        """Test that each instance has a unique id"""
        models = [BaseModel() for _ in range(1000)]
        ids = [model.id for model in models]
        self.assertEqual(len(ids), len(set(ids)))  # No duplicate IDs

    def test_instance_creation_time(self):
        """Test that instances created at different times have different timestamps"""
        model1 = BaseModel()
        sleep(0.1)
        model2 = BaseModel()
        self.assertLess(model1.created_at, model2.created_at)

    def test_public_attributes(self):
        """Test that all required public attributes exist"""
        attrs = ['id', 'created_at', 'updated_at']
        for attr in attrs:
            self.assertTrue(hasattr(self.base, attr))
            self.assertFalse(attr.startswith('_'))

    def test_attribute_types(self):
        """Test that attributes are of correct type"""
        self.assertIsInstance(self.base.id, str)
        self.assertIsInstance(self.base.created_at, datetime)
        self.assertIsInstance(self.base.updated_at, datetime)
        self.assertEqual(len(self.base.id), 36)  # UUID length

    def test_datetime_precision(self):
        """Test datetime precision in the model"""
        model = BaseModel()
        dict_model = model.to_dict()
        # Ensure microseconds are preserved
        self.assertIn('.', dict_model['created_at'])
        self.assertIn('.', dict_model['updated_at'])

    def test_kwargs_none_values(self):
        """Test handling of None values in kwargs"""
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)

    def test_storage_interaction(self):
        """Test interaction with storage system"""
        self.base.name = "Test Storage"
        self.base.save()
        key = f"BaseModel.{self.base.id}"
        self.assertIn(key, storage.all())
        stored_obj = storage.all()[key]
        self.assertEqual(stored_obj.name, "Test Storage")

    def test_to_dict_not_return_dict_copy(self):
        """Test that to_dict returns a new dict and not a reference"""
        self.base.name = "Test"
        base_dict = self.base.to_dict()
        base_dict['name'] = "Modified"
        self.assertEqual(self.base.name, "Test")

    def test_dynamic_attribute_handling(self):
        """Test handling of dynamically added attributes"""
        self.base.dynamic_attr = "Dynamic"
        base_dict = self.base.to_dict()
        self.assertIn('dynamic_attr', base_dict)
        self.assertEqual(base_dict['dynamic_attr'], "Dynamic")
