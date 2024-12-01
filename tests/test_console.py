#!/usr/bin/python3
"""
Comprehensive unit tests for HBNBCommand console.
Tests all possible edge cases and scenarios for the new version.
"""

import unittest
from unittest.mock import patch
from io import StringIO
import sys
import os
from console import HBNBCommand, parse
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
import pep8
import console


class TestHBNBCommand(unittest.TestCase):
    """Test cases for HBNBCommand console"""

    @classmethod
    def setUpClass(cls):
        """Set up class test environment"""
        cls.console = HBNBCommand()

    def setUp(self):
        """Set up test environment"""
        try:
            os.remove("file.json")
        except:
            pass
        storage._FileStorage__objects = {}

    def tearDown(self):
        """Clean up test environment"""
        try:
            os.remove("file.json")
        except:
            pass

    def test_pep8_conformance(self):
        """Test PEP8 conformance"""
        style_guide = pep8.StyleGuide(quiet=True)
        result = style_guide.check_files(['console.py',
                                          'tests/test_console.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_docstrings(self):
        """Test docstrings"""
        self.assertIsNotNone(console.__doc__)
        self.assertIsNotNone(HBNBCommand.__doc__)
        self.assertIsNotNone(HBNBCommand.do_quit.__doc__)
        self.assertIsNotNone(HBNBCommand.do_EOF.__doc__)
        self.assertIsNotNone(HBNBCommand.do_create.__doc__)
        self.assertIsNotNone(HBNBCommand.do_show.__doc__)
        self.assertIsNotNone(HBNBCommand.do_destroy.__doc__)
        self.assertIsNotNone(HBNBCommand.do_all.__doc__)
        self.assertIsNotNone(HBNBCommand.do_update.__doc__)
        self.assertIsNotNone(HBNBCommand.do_count.__doc__)

    def test_parse(self):
        """Test command argument parsing"""
        # Test basic parsing
        self.assertEqual(parse("BaseModel 1234-1234"),
                         ["BaseModel", "1234-1234"])
        # Test parsing with curly braces
        self.assertEqual(parse('BaseModel 1234-1234 {"name": "John"}'),
                         ["BaseModel", "1234-1234", '{"name": "John"}'])
        # Test parsing with brackets
        self.assertEqual(parse("BaseModel 1234-1234 [1, 2, 3]"),
                         ["BaseModel", "1234-1234", "[1, 2, 3]"])
        # Test parsing with commas
        self.assertEqual(parse("BaseModel, 1234-1234, name, John"),
                         ["BaseModel", "1234-1234", "name", "John"])

    def test_emptyline(self):
        """Test empty line input"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("")
            self.assertEqual("", f.getvalue().strip())

    def test_quit_and_EOF(self):
        """Test quit and EOF commands"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertTrue(HBNBCommand().onecmd("quit"))
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertTrue(HBNBCommand().onecmd("EOF"))

    def test_create(self):
        """Test create command"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create")
            self.assertEqual("** class name missing **", f.getvalue().strip())

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create MyModel")
            self.assertEqual("** class doesn't exist **", f.getvalue().strip())

        for class_name in HBNBCommand.valid_classes:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"create {class_name}")
                self.assertIsInstance(f.getvalue().strip(), str)
                self.assertGreater(len(f.getvalue().strip()), 0)

    def test_show(self):
        """Test show command"""
        # Test with missing class name
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show")
            self.assertEqual("** class name missing **", f.getvalue().strip())

        # Test with invalid class name
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show MyModel")
            self.assertEqual("** class doesn't exist **", f.getvalue().strip())

        # Test with missing instance id
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show BaseModel")
            self.assertEqual("** instance id missing **", f.getvalue().strip())

        # Test with invalid instance id
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show BaseModel 1234-1234")
            self.assertEqual("** no instance found **", f.getvalue().strip())

    def test_destroy(self):
        """Test destroy command"""
        # Test with missing class name
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy")
            self.assertEqual("** class name missing **", f.getvalue().strip())

        # Test with invalid class name
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy MyModel")
            self.assertEqual("** class doesn't exist **", f.getvalue().strip())

        # Test with missing instance id
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy BaseModel")
            self.assertEqual("** instance id missing **", f.getvalue().strip())

    def test_all(self):
        """Test all command"""
        # Test with invalid class name
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all MyModel")
            self.assertEqual("** class doesn't exist **", f.getvalue().strip())

        # Test all with valid class
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
            HBNBCommand().onecmd("all BaseModel")
            self.assertIn("BaseModel", f.getvalue())

    def test_count(self):
        """Test count command"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
            HBNBCommand().onecmd("count BaseModel")
            self.assertEqual("1", f.getvalue().strip().split('\n')[-1])

    def test_update(self):
        """Test update command"""
        # Test with missing class name
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update")
            self.assertEqual("** class name missing **", f.getvalue().strip())

        # Test with invalid class name
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update MyModel")
            self.assertEqual("** class doesn't exist **", f.getvalue().strip())

        # Test with missing instance id
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update BaseModel")
            self.assertEqual("** instance id missing **", f.getvalue().strip())

    def test_default(self):
        """Test default command handling"""
        # Test invalid syntax
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("BaseModel.invalid()")
            self.assertEqual("*** Unknown syntax: BaseModel.invalid()",
                             f.getvalue().strip())

        # Test valid class methods
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
            model_id = f.getvalue().strip()

            # Test show
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f'BaseModel.show("{model_id}")')
                self.assertIn("BaseModel", f.getvalue())

            # Test count
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd("BaseModel.count()")
                self.assertEqual("1", f.getvalue().strip())

            # Test destroy
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f'BaseModel.destroy("{model_id}")')
                self.assertEqual("", f.getvalue().strip())

    def test_alternate_syntax(self):
        """Test alternate command syntax (e.g., User.all())"""
        for class_name in HBNBCommand.valid_classes:
            # Test .all()
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"{class_name}.all()")
                self.assertIsInstance(eval(f.getvalue()), list)

            # Test .count()
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"{class_name}.count()")
                self.assertTrue(f.getvalue().strip().isdigit())

            # Create an instance for further testing
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"create {class_name}")
                obj_id = f.getvalue().strip()

            # Test .show()
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f'{class_name}.show("{obj_id}")')
                self.assertIn(class_name, f.getvalue())

            # Test .destroy()
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f'{class_name}.destroy("{obj_id}")')
                self.assertEqual("", f.getvalue().strip())

    def test_update_with_dictionary(self):
        """Test update command with dictionary input"""
        # Create an instance
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
            obj_id = f.getvalue().strip()

        # Test update with dictionary
        with patch('sys.stdout', new=StringIO()) as f:
            update_cmd = f'BaseModel.update("{obj_id}", ' + \
                '{"name": "test_name", "value": 100})'
            HBNBCommand().onecmd(update_cmd)

            # Verify the update
            HBNBCommand().onecmd(f'BaseModel.show("{obj_id}")')
            self.assertIn("test_name", f.getvalue())
            self.assertIn("100", f.getvalue())


if __name__ == "__main__":
    unittest.main()
