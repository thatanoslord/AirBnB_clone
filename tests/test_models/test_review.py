#!/usr/bin/env python3
"""
Unit Test Module for Review Class
"""
import unittest
from models.review import Review
from models.base_model import BaseModel
import models
import os


class TestReview(unittest.TestCase):
    """Test cases for the Review class"""

    def setUp(self):
        """Set up test methods"""
        self.review = Review()

    def tearDown(self):
        """Clean up after test methods"""
        try:
            os.remove("file.json")
        except:
            pass

    def test_review_inheritance(self):
        """Test if Review inherits from BaseModel"""
        self.assertIsInstance(self.review, BaseModel)
        self.assertTrue(hasattr(self.review, "id"))
        self.assertTrue(hasattr(self.review, "created_at"))
        self.assertTrue(hasattr(self.review, "updated_at"))

    def test_review_attributes(self):
        """Test Review class attributes"""
        self.assertTrue(hasattr(self.review, "place_id"))
        self.assertTrue(hasattr(self.review, "user_id"))
        self.assertTrue(hasattr(self.review, "text"))
        self.assertEqual(self.review.place_id, "")
        self.assertEqual(self.review.user_id, "")
        self.assertEqual(self.review.text, "")

    def test_review_attribute_assignment(self):
        """Test attribute assignment"""
        test_place_id = "place-123"
        test_user_id = "user-123"
        test_text = "Great place to stay!"

        self.review.place_id = test_place_id
        self.review.user_id = test_user_id
        self.review.text = test_text

        self.assertEqual(self.review.place_id, test_place_id)
        self.assertEqual(self.review.user_id, test_user_id)
        self.assertEqual(self.review.text, test_text)

    def test_to_dict_method(self):
        """Test to_dict method"""
        self.review.place_id = "place-123"
        self.review.user_id = "user-123"
        self.review.text = "Amazing experience!"
        review_dict = self.review.to_dict()

        self.assertIsInstance(review_dict, dict)
        self.assertEqual(review_dict['__class__'], 'Review')
        self.assertEqual(review_dict['place_id'], "place-123")
        self.assertEqual(review_dict['user_id'], "user-123")
        self.assertEqual(review_dict['text'], "Amazing experience!")
        self.assertIsInstance(review_dict['created_at'], str)
        self.assertIsInstance(review_dict['updated_at'], str)

    def test_str_representation(self):
        """Test string representation"""
        string = str(self.review)
        self.assertIn("[Review]", string)
        self.assertIn("id", string)

    def test_review_save(self):
        """Test save method"""
        old_updated_at = self.review.updated_at
        self.review.save()
        self.assertNotEqual(old_updated_at, self.review.updated_at)
