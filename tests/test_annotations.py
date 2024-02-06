import unittest
from typing import List, Optional, Set

from simple_animl.core import Field, XmlModel
from simple_animl.core.annotations import Annotation


class A:
    "Test type"
    pass


class B:
    "Test type 2"
    pass


class TestGeneral(unittest.TestCase):
    def test_Model(self):
        A = "my_annotation_as_string"

        class Model_A(XmlModel):
            # pylint: disable=reportUndefinedVariable
            name: A = Field.Attribute()

        self.assertEqual(Model_A._fields[0].name, "name")
        self.assertEqual(Model_A._fields[0].annotation._type, A)


class TestPythonTypes(unittest.TestCase):
    def test_TypesOK(self):
        tests = [
            (str, str),
            (A, A),
            (list[str], str),
        ]

        for test in tests:
            with self.subTest(test=f"{'Annotation'}: '{test[0]}'"):
                ann = Annotation.parse(test[0])
                self.assertEqual(test[1], ann._type)

    def test_isList(self):
        ann = Annotation.parse(list[A])
        self.assertEqual(ann._type, A)
        self.assertTrue(ann.isList)
        self.assertFalse(ann.isOptional)


class TestStringTypes(unittest.TestCase):
    def test_TypesOK(self):
        tests = [
            ("str", "str"),
            ("anything_", "anything_"),
            ("list[str]", "str"),
        ]

        for test in tests:
            with self.subTest(test=f"{'Annotation'}: '{test[0]}'"):
                ann = Annotation.parse(test[0])
                self.assertEqual(test[1], ann._type)

    def test_isList(self):
        ann = Annotation.parse("list[A]")
        self.assertEqual(ann._type, "A")
        self.assertTrue(ann.isList)
        self.assertFalse(ann.isOptional)

    def test_SyntaxCheck(self):
        # Make sure correct error is raised
        tests = [
            "str-2",
            " str",
            "int ",
            "MyType-3",
        ]

        for test in tests:
            with self.subTest(test=f"{'Bad annotation'}: '{test}'"):
                f1 = lambda: Annotation.parse(test)
                self.assertRaisesRegex(SyntaxError, "Invalid type syntax:", f1)


class TestTypingLibTypes(unittest.TestCase):
    def test_TypesOK(self):
        tests = [
            (Optional[str], str),
            (List[Optional[str]], str),
            (Optional[List[A]], A),
        ]

        for test in tests:
            with self.subTest(test=f"{'Annotation'}: '{test[0]}'"):
                ann = Annotation.parse(test[0])
                self.assertEqual(test[1], ann._type)

    def test_isList(self):
        ann = Annotation.parse(List[A])
        self.assertEqual(ann._type, A)
        self.assertTrue(ann.isList)
        self.assertFalse(ann.isOptional)

    def test_isOptional(self):
        ann = Annotation.parse(Optional[A])
        self.assertEqual(ann._type, A)
        self.assertFalse(ann.isList)
        self.assertTrue(ann.isOptional)

    def test_isOptionalList(self):
        ann = Annotation.parse(Optional[List[A]])
        self.assertEqual(ann._type, A)
        self.assertTrue(ann.isList)
        self.assertTrue(ann.isOptional)

    def test_UnsupportedTypes(self):
        # Make sure correct error is raised
        f1 = lambda: Annotation.parse(Set[A])
        self.assertRaisesRegex(TypeError, "Unsupported typing type:", f1)
