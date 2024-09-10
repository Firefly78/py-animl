import unittest
from dataclasses import dataclass
from enum import Enum
from typing import Annotated

from helpers import create_dummy_regclass, make_element

from animl2.core.base import XmlModel
from animl2.core.fields import ATTRIB


class TestEnum(unittest.TestCase):

    def test_dump(self):
        """Validate the enums are serialized correctly"""

        regclass = create_dummy_regclass()

        class MyEnum(str, Enum):
            A = "a"
            B = "b"

        regclass.register(MyEnum.__name__, MyEnum)

        @dataclass
        class ModelA(XmlModel, regclass=regclass):
            value: Annotated[MyEnum, ATTRIB]

        x = ModelA(value=MyEnum.A)  # Model holding an enum
        value = x.dump_xml().attrib["value"]

        self.assertIsInstance(value, str)
        self.assertNotIsInstance(value, MyEnum)  # Make sure pure string is in the XML
        self.assertEqual(value, "a")

    def test_load(self):
        """Validate the enums are deserialized correctly"""

        regclass = create_dummy_regclass()

        class MyEnum(str, Enum):
            A = "a"
            B = "b"

        regclass.register(MyEnum.__name__, MyEnum)

        @dataclass
        class ModelA(XmlModel, regclass=regclass):
            value: Annotated[MyEnum, ATTRIB]

        element = make_element(
            "ModelA", attrib={"value": "b"}
        )  # XML element with a string attribute
        x = ModelA.load_xml(element)
        value = x.value

        self.assertIsInstance(value, MyEnum)  # Model should contain an enum
        self.assertEqual(value, MyEnum.B)
