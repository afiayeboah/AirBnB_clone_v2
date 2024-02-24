#!/usr/bin/python3
"""
Contains the TestBaseModel class
"""
import unittest
import datetime
import json
import os
import pycodestyle
import inspect
from models.base_model import BaseModel
from uuid import UUID


class TestBaseModel(unittest.TestCase):
    """
    A class to test BaseModel
    """

    @classmethod
    def setUpClass(cls):
        """
        Setup for the test
        """
        cls.base = BaseModel()
        cls.base.name = "Kev"
        cls.base.num = 20

    @classmethod
    def tearDownClass(cls):
        """
        Clean up after all tests
        """
        del cls.base
        try:
            os.remove("file.json")
        except Exception:
            pass

    def tearDown(self):
        """
        Clean up after each test
        """
        try:
            os.remove("file.json")
        except Exception:
            pass

    def test_pep8_BaseModel(self):
        """
        Test for PEP8 compliance
        """
        style = pycodestyle.StyleGuide(quiet=True)
        result = style.check_files(['models/base_model.py'])
        self.assertEqual(result.total_errors, 0, "PEP8 style errors found")

    def test_checking_for_docstring_BaseModel(self):
        """
        Test docstrings
        """
        self.assertIsNotNone(BaseModel.__doc__)
        self.assertIsNotNone(BaseModel.__init__.__doc__)
        self.assertIsNotNone(BaseModel.__str__.__doc__)
        self.assertIsNotNone(BaseModel.save.__doc__)
        self.assertIsNotNone(BaseModel.to_dict.__doc__)

    def test_method_BaseModel(self):
        """
        Test if BaseModel has methods
        """
        self.assertTrue(hasattr(BaseModel, "__init__"))
        self.assertTrue(hasattr(BaseModel, "save"))
        self.assertTrue(hasattr(BaseModel, "to_dict"))

    def test_init_BaseModel(self):
        """
        Test if the base is an instance of BaseModel
        """
        self.assertIsInstance(self.base, BaseModel)

    def test_save_BaesModel(self):
        """
        Test if the save method works
        """
        self.base.save()
        self.assertNotEqual(self.base.created_at, self.base.updated_at)

    def test_to_dict_BaseModel(self):
        """
        Test if to_dict method returns correct dictionary
        """
        base_dict = self.base.to_dict()
        self.assertEqual(base_dict["__class__"], "BaseModel")
        self.assertIsInstance(base_dict["created_at"], str)
        self.assertIsInstance(base_dict["updated_at"], str)

    def test_uuid(self):
        """
        Test UUID generation
        """
        instance1 = BaseModel()
        instance2 = BaseModel()
        instance3 = BaseModel()
        list_instances = [instance1, instance2, instance3]
        for instance in list_instances:
            self.assertIsInstance(UUID(instance.id), UUID)
        self.assertNotEqual(instance1.id, instance2.id)
        self.assertNotEqual(instance1.id, instance3.id)
        self.assertNotEqual(instance2.id, instance3.id)

    def test_str_method(self):
        """
        Test __str__ method
        """
        instance = BaseModel()
        expected_output = "[BaseModel] ({}) {}".format(instance.id,
                                                       instance.__dict__)
        self.assertEqual(str(instance), expected_output)

    def test_dict_to_instance(self):
        """
        Test creating instance from dictionary
        """
        instance = BaseModel()
        instance.save()
        instance_dict = instance.to_dict()
        new_instance = BaseModel(**instance_dict)
        self.assertNotEqual(instance, new_instance)
        self.assertEqual(instance.id, new_instance.id)
        self.assertEqual(instance.created_at, new_instance.created_at)
        self.assertEqual(instance.updated_at, new_instance.updated_at)

    def test_extra_attributes(self):
        """
        Test creating instance with extra attributes
        """
        instance = BaseModel()
        instance.extra = "extra_attribute"
        instance.save()
        instance_dict = instance.to_dict()
        new_instance = BaseModel(**instance_dict)
        self.assertTrue(hasattr(new_instance, "extra"))
        self.assertEqual(new_instance.extra, "extra_attribute")


if __name__ == "__main__":
    unittest.main()

