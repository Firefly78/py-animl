import unittest
import xml.etree.ElementTree as etree
from typing import List, Optional, Set, Union

from helpers import create_dummy_regclass

from animl2.core import Field, XmlModel
from animl2.core.annotations import Annotation


class A:
    "Test type"
    pass


class B:
    "Test type 2"
    pass


class TestGeneral(unittest.TestCase):
    def test_Model(self):
        A = "my_annotation_as_string"

        class Model_A(XmlModel, regclass=create_dummy_regclass()):
            # pylint: disable=reportUndefinedVariable
            name: A = Field.Attribute()

        self.assertEqual(Model_A._fields[0].name, "name")
        self.assertEqual(Model_A._fields[0].annotation.tType, A)


class TestPythonTypes(unittest.TestCase):
    def test_TypesOK(self):
        tests = [
            (str, str),
            (A, A),
            (list[str], list),
        ]

        for test in tests:
            with self.subTest(test=f"{'Annotation'}: '{test[0]}'"):
                ann = Annotation.parse(test[0])
                self.assertTrue(ann.validtype(test[1]))
                self.assertEqual(test[1], ann.tType)

    def test_isList(self):
        ann = Annotation.parse(list[A])
        self.assertEqual(ann.tType, list)
        self.assertTrue(any([x.validtype(A) for x in ann.subType]))


class TestStringTypes(unittest.TestCase):
    def test_TypesOK(self):
        tests = [
            ("str", "str"),
            ("anything_", "anything_"),
        ]

        for test in tests:
            with self.subTest(test=f"{'Annotation'}: '{test[0]}'"):
                ann = Annotation.parse(test[0])
                self.assertEqual(test[1], ann.tType)
                self.assertTrue(ann.validtype(test[1]))

    def test_isList(self):
        ann = Annotation.parse("list[A]")
        self.assertEqual(ann.tType, list)
        self.assertTrue(ann.validsubtype(A))
        self.assertFalse(ann.validtype(None))
        self.assertTrue(ann.isList)
        self.assertFalse(ann.isOptional)

    def test_isOptional(self):
        ann = Annotation.parse("Optional[A]")
        self.assertEqual(ann.tType, Union)
        self.assertTrue(ann.validtype(A))
        self.assertTrue(ann.validtype(None))
        self.assertFalse(ann.isList)
        self.assertTrue(ann.isOptional)

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
    def test_isList(self):
        ann = Annotation.parse(List[A])
        self.assertEqual(ann.tType, list)
        self.assertTrue(ann.validsubtype(A))
        self.assertFalse(ann.validsubtype(None))

    def test_isListOptional(self):
        ann = Annotation.parse(List[Optional[A]])
        self.assertEqual(ann.tType, list)
        self.assertTrue(ann.validsubtype(A))
        self.assertTrue(ann.validsubtype(None))

    def test_isOptional(self):
        ann = Annotation.parse(Optional[A])
        self.assertEqual(ann.tType, Union)
        self.assertTrue(ann.validtype(A))

    def test_isOptionalList(self):
        ann = Annotation.parse(Optional[List[A]])
        self.assertEqual(ann.tType, Union)
        self.assertTrue(ann.validtype(list))
        self.assertTrue(ann.validtype(None))
        self.assertTrue(ann.subType[0].validsubtype(A))

    def test_UnsupportedTypes(self):
        # Make sure correct error is raised
        f1 = lambda: Annotation.parse(Set[A])
        self.assertRaisesRegex(TypeError, "Unsupported typing type:", f1)


class TestUnionTypes(unittest.TestCase):
    def test_Model(self):
        regclass = create_dummy_regclass()

        class TestUnionTypesA(XmlModel, regclass=regclass):
            pass

        class TestUnionTypesB(XmlModel, regclass=regclass):
            pass

        class TestUnionTypesC(XmlModel, regclass=regclass):
            pass

        class UnionModel(XmlModel, regclass=regclass):
            child_either_A_or_B: Union[
                TestUnionTypesA, TestUnionTypesB, TestUnionTypesC
            ] = Field.Child()

        self.assertEqual(UnionModel._fields[0].name, "child_either_A_or_B")
        self.assertTrue(UnionModel._fields[0].annotation.validtype(TestUnionTypesA))
        self.assertTrue(UnionModel._fields[0].annotation.validtype(TestUnionTypesB))
        self.assertTrue(UnionModel._fields[0].annotation.validtype(TestUnionTypesC))

    def test_Load(self):
        regclass = create_dummy_regclass()

        class TestUnionTypesD(XmlModel, regclass=regclass):
            tag = "DD"

        class TestUnionTypesE(XmlModel, regclass=regclass):
            tag = "EE"

        class TestUnionLoadModel(XmlModel, regclass=regclass):
            child: Union[TestUnionTypesD, TestUnionTypesE] = Field.Child()

        xml1 = "<TestUnionLoadModel><DD/></TestUnionLoadModel>"
        TestUnionLoadModel.load_xml(etree.fromstring(xml1))

        xml2 = "<TestUnionLoadModel><EE/></TestUnionLoadModel>"
        TestUnionLoadModel.load_xml(etree.fromstring(xml2))
