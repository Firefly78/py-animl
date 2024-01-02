import unittest

from simple_animl.core.base import XmlModel
from simple_animl.core.fields import Field


class TestAttribute(unittest.TestCase):
    def test_Alias(self):
        self.assertEqual(Field.Attribute(alias="my-alias").alias, "my-alias")

        self.assertRaisesRegex(
            TypeError,
            "alias must be a string or None",
            lambda: Field.Attribute(alias=1),
        )

    def test_Default(self):
        tests = [
            ({}, None, "No default"),
            ({"default": "def-1"}, "def-1", "Default as value"),
            ({"default_factory": lambda: "def-1"}, "def-1", "Default as factory"),
        ]

        for test in tests:
            with self.subTest(test=test[2]):
                field = Field.Attribute(**test[0])
                self.assertEqual(field.has_default(), test[1] is not None)
                self.assertEqual(field.get_default(), test[1])


class TestBase(unittest.TestCase):
    def test_ABC(self):
        self.assertRaises(TypeError, lambda: Field.Base())


class TestChild(unittest.TestCase):
    def test_Default(self):
        tests = [
            ({}, None, "No default"),
            ({"default": XmlModel}, XmlModel, "Default as value"),
            ({"default_factory": lambda: XmlModel}, XmlModel, "Default as factory"),
        ]

        for test in tests:
            with self.subTest(test=test[2]):
                field = Field.Child(**test[0])
                self.assertEqual(field.has_default(), test[1] is not None)
                self.assertEqual(field.get_default(), test[1])


class TestText(unittest.TestCase):
    def test_Default(self):
        tests = [
            ({}, None, "No default"),
            ({"default": "def-1"}, "def-1", "Default as value"),
            ({"default_factory": lambda: "def-1"}, "def-1", "Default as factory"),
        ]

        for test in tests:
            with self.subTest(test=test[2]):
                field = Field.Text(**test[0])
                self.assertEqual(field.has_default(), test[1] is not None)
                self.assertEqual(field.get_default(), test[1])
