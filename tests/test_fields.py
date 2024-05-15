import unittest
import xml.etree.ElementTree as etree
from enum import Enum

from helpers import create_dummy_regclass

from simple_animl.core.base import XmlModel
from simple_animl.core.fields import Field
from simple_animl.utils.regex import NC_NAME


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

    def test_Validate_Dump(self):
        class A_ValidateDump(XmlModel, regclass=create_dummy_regclass()):
            value: str = Field.Attribute(regex=NC_NAME)

        # OK
        A_ValidateDump(value="good-value").dump_xml()
        # Bad
        self.assertRaisesRegex(
            ValueError,
            "value must match regex",
            lambda: A_ValidateDump(value="0bad-value").dump_xml(),
        )

    def test_Validate_Init(self):
        class A_ValidateInit(XmlModel, regclass=create_dummy_regclass()):
            value: str = Field.Attribute(regex=NC_NAME)

        # OK
        A_ValidateInit(value="good-value")
        # Bad
        self.assertRaisesRegex(
            ValueError,
            "value must match regex",
            lambda: A_ValidateInit(value="0bad-value"),
        )

    def test_Validate_Load(self):
        class A_ValidateLoad(XmlModel, regclass=create_dummy_regclass()):
            value: str = Field.Attribute(regex=NC_NAME)

        # OK
        A_ValidateLoad.load_xml(
            etree.fromstring("<A_ValidateLoad value='good-value' />")
        )
        # Bad
        self.assertRaisesRegex(
            ValueError,
            "value must match regex",
            lambda: A_ValidateLoad.load_xml(
                etree.fromstring("<A_ValidateLoad value='0bad-value' />")
            ),
        )


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

    def test_Enum_Deserialize(self):
        class MyEnumED(str, Enum):
            VALUE1 = "this-is-my-text"

        regclass = create_dummy_regclass()

        regclass.register(MyEnumED.__name__, MyEnumED)

        class B(XmlModel, regclass=regclass):
            value: MyEnumED = Field.Text()

        xml_string = "<B>this-is-my-text</B>"
        root = etree.fromstring(xml_string)
        b = B.load_xml(root)
        self.assertEqual(b.value, MyEnumED.VALUE1)

    def test_Enum_DeserializeEx(self):
        class MyEnumEDE(str, Enum):
            VALUE1 = "this-is-my-text"

        regclass = create_dummy_regclass()
        regclass.register(MyEnumEDE.__name__, MyEnumEDE)

        class B2(XmlModel, regclass=regclass):
            value: MyEnumEDE = Field.Text()

        xml_string = "<B2>bad-string</B2>"
        root = etree.fromstring(xml_string)
        self.assertRaisesRegex(ValueError, "bad-string", lambda: B2.load_xml(root))

    def test_Enum_Serialize(self):
        class MyEnumES(str, Enum):
            VALUE1 = "this-is-my-text"

        regclass = create_dummy_regclass()
        regclass.register(MyEnumES.__name__, MyEnumES)

        class ES(XmlModel, regclass=regclass):
            value: MyEnumES = Field.Text()  # Use enum as field

        m = ES(value=MyEnumES.VALUE1)

        xml = m.dump_xml()

        self.assertEqual(xml.text, MyEnumES.VALUE1.value)

    def test_Enum_SerializeEx(self):
        class MyEnumESE(Enum):
            VALUE1 = "this-is-my-text"

        regclass = create_dummy_regclass()
        regclass.register(MyEnumESE.__name__, MyEnumESE)

        class ESE(XmlModel, regclass=regclass):
            value: MyEnumESE = Field.Text()  # Use enum as field

        m = ESE(value=MyEnumESE.VALUE1)

        self.assertRaisesRegex(TypeError, "Type must be string", lambda: m.dump_xml())

    def test_Validate_Dump(self):
        class A_ValidateTDump(XmlModel, regclass=create_dummy_regclass()):
            value: str = Field.Text(regex=NC_NAME)

        # OK
        A_ValidateTDump(value="good-value").dump_xml()
        # Bad
        self.assertRaisesRegex(
            ValueError,
            "value must match regex",
            lambda: A_ValidateTDump(value="0bad-value").dump_xml(),
        )

    def test_Validate_Init(self):
        class A_ValidateTInit(XmlModel, regclass=create_dummy_regclass()):
            value: str = Field.Text(regex=NC_NAME)

        # OK
        A_ValidateTInit(value="good-value")
        # Bad
        self.assertRaisesRegex(
            ValueError,
            "value must match regex",
            lambda: A_ValidateTInit(value="0bad-value"),
        )

    def test_Validate_Load(self):
        class A_ValidateTLoad(XmlModel, regclass=create_dummy_regclass()):
            value: str = Field.Text(regex=NC_NAME)

        # OK
        A_ValidateTLoad.load_xml(
            etree.fromstring("<A_ValidateTLoad>good-value</A_ValidateTLoad>")
        )
        # Bad
        self.assertRaisesRegex(
            ValueError,
            "value must match regex",
            lambda: A_ValidateTLoad.load_xml(
                etree.fromstring("<A_ValidateTLoad>0bad-value</A_ValidateTLoad>")
            ),
        )
