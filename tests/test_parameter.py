import unittest
from xml.etree.ElementTree import Element

from helpers import make_element

from animl2.core import XmlModel
from animl2.models.data_type import IntType
from animl2.models.parameter import Parameter, ParameterType
from animl2.models.unit import Unit


class TestParameter(unittest.TestCase):
    def test_Inheritance(self):
        self.assertTrue(issubclass(Parameter, XmlModel))

    def test_Dump(self):
        obj = Parameter(
            name="Parameter 1",
            parameterType=ParameterType.Int32,
            id="param1",
            value=IntType(value=42),
            unit=Unit(label="m"),
        )
        xml = obj.dump_xml()

        self.assertIsNotNone(xml)
        self.assertEqual(xml.tag, "Parameter")
        self.assertEqual(xml.attrib["name"], "Parameter 1")
        self.assertEqual(xml.attrib["parameterType"], "Int32")
        self.assertEqual(xml.attrib["id"], "param1")

        self.assertEqual(xml.find("I").text, "42")
        self.assertEqual(xml.find("Unit").attrib["label"], "m")

    def test_Load(self):
        xml = Element("Parameter")
        xml.attrib["name"] = "Parameter 1"
        xml.attrib["parameterType"] = "Int32"
        xml.attrib["id"] = "param1"
        xml.append(make_element("I", text="42"))
        xml.append(make_element("Unit", attrib={"label": "m"}))

        obj = Parameter.load_xml(xml)
        self.assertIsInstance(obj, Parameter)
        self.assertEqual(obj.name, "Parameter 1")
        self.assertEqual(obj.parameterType, ParameterType.Int32)
        self.assertEqual(obj.id, "param1")

        self.assertIsInstance(obj.value, IntType)
        self.assertEqual(obj.value.value, 42)

        self.assertIsInstance(obj.unit, Unit)
        self.assertEqual(obj.unit.label, "m")
