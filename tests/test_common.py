import unittest
from xml.etree.ElementTree import Element

from animl2.core import XmlModel
from animl2.models.common import Manufacturer, Name


class TestManufacturer(unittest.TestCase):
    def test_Inheritance(self):
        self.assertTrue(issubclass(Manufacturer, XmlModel))

    def test_Dump(self):
        obj = Manufacturer(value="ACME Corp")
        xml = obj.dump_xml()

        self.assertIsNotNone(xml)
        self.assertEqual(xml.tag, "Manufacturer")
        self.assertEqual(xml.text, "ACME Corp")

    def test_Load(self):
        xml = Element("Manufacturer")
        xml.text = "ACME Corp"

        obj = Manufacturer.load_xml(xml)
        self.assertIsInstance(obj, Manufacturer)
        self.assertEqual(obj.value, "ACME Corp")


class TestName(unittest.TestCase):
    def test_Inheritance(self):
        self.assertTrue(issubclass(Name, XmlModel))

    def test_Dump(self):
        obj = Name(value="John Doe")
        xml = obj.dump_xml()

        self.assertIsNotNone(xml)
        self.assertEqual(xml.tag, "Name")
        self.assertEqual(xml.text, "John Doe")

    def test_Load(self):
        xml = Element("Name")
        xml.text = "John Doe"

        obj = Name.load_xml(xml)
        self.assertIsInstance(obj, Name)
        self.assertEqual(obj.value, "John Doe")
