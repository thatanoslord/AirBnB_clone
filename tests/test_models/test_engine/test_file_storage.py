#!/usr/bin/python3
"""
Comprehensive unit tests for FileStorage class.
Tests all possible edge cases and scenarios.
"""

from unittest.mock import patch
from models.engine.file_storage import FileStorage
import unittest
from models.base_model import BaseModel
from models import storage
from time import sleep
import os
import json


class TestFileStorage(unittest.TestCase):
    """Test cases for FileStorage class"""

    def setUp(self):
        """Set up test environment"""
        try:
            os.remove("file.json")
        except:
            pass
        self.storage = FileStorage()
        self.model = BaseModel()

    def tearDown(self):
        """Clean up test environment"""
        try:
            os.remove("file.json")
        except:
            pass

    def test_file_path(self):
        """Test file path attribute"""
        self.assertEqual(FileStorage._FileStorage__file_path, "file.json")

    def test_objects_dict(self):
        """Test objects dictionary attribute"""
        self.assertIsInstance(FileStorage._FileStorage__objects, dict)

    def test_all_method(self):
        """Test all() method"""
        all_objs = self.storage.all()
        self.assertIsInstance(all_objs, dict)
        self.assertEqual(all_objs, FileStorage._FileStorage__objects)

    def test_new_method(self):
        """Test new() method"""
        model = BaseModel()
        self.storage.new(model)
        key = f"BaseModel.{model.id}"
        self.assertIn(key, FileStorage._FileStorage__objects)

    def test_new_with_none(self):
        """Test new() method with None"""
        with self.assertRaises(AttributeError):
            self.storage.new(None)

    def test_save_and_reload(self):
        """Test save() and reload() methods"""
        model = BaseModel()
        model.name = "Test Model"
        self.storage.new(model)
        self.storage.save()

        # Clear objects and reload
        FileStorage._FileStorage__objects = {}
        self.storage.reload()

        key = f"BaseModel.{model.id}"
        self.assertIn(key, FileStorage._FileStorage__objects)
        reloaded_model = FileStorage._FileStorage__objects[key]
        self.assertEqual(reloaded_model.name, "Test Model")

    def test_reload_from_nonexistent_file(self):
        """Test reload() with nonexistent file"""
        try:
            os.remove("file.json")
        except:
            pass
        self.assertEqual(self.storage.reload(), None)

    def test_reload_from_empty_file(self):
        """Test reload() with empty file"""
        prev_len = len(FileStorage._FileStorage__objects)
        with open("file.json", "w") as f:
            f.write("{}")
        self.storage.reload()
        self.assertEqual(len(FileStorage._FileStorage__objects), prev_len)

    def test_reload_with_invalid_json(self):
        """Test reload() with invalid JSON"""
        with open("file.json", "w") as f:
            f.write("{invalid json}")
        with self.assertRaises(json.JSONDecodeError):
            self.storage.reload()

    def test_multiple_saves(self):
        """Test multiple saves"""
        models = [BaseModel() for _ in range(10)]
        for model in models:
            self.storage.new(model)
            self.storage.save()

        self.storage.reload()
        for model in models:
            key = f"BaseModel.{model.id}"
            self.assertIn(key, FileStorage._FileStorage__objects)

    # def test_storage_file_permissions(self):
    #     """Test file permissions handling"""
    #     self.storage.save()
    #     os.chmod("file.json", 0o444)  # Read-only

    #     model = BaseModel()
    #     self.storage.new(model)
    #     with self.assertRaises(PermissionError):
    #         self.storage.save()

    #     os.chmod("file.json", 0o666)  # Restore permissions

    def test_storage_file_corruption(self):
        """Test handling of corrupted storage file"""
        self.storage.save()
        with open("file.json", "w") as f:
            f.write("corrupted data")

        with self.assertRaises(json.JSONDecodeError):
            self.storage.reload()

    def test_large_data_handling(self):
        """Test handling of large amounts of data"""
        prev_len = len(FileStorage._FileStorage__objects)
        # print(f"prev_len: {prev_len}")
        models = [BaseModel() for _ in range(1000)]
        for model in models:
            self.storage.new(model)
        self.storage.save()

        # Clear and reload
        FileStorage._FileStorage__objects = {}
        self.storage.reload()
        self.assertEqual(
            len(FileStorage._FileStorage__objects), prev_len + 1000)
