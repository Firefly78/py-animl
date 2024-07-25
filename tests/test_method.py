import unittest
from xml.etree.ElementTree import Element

from animl2.core import XmlModel
from animl2.models.method import Method


class TestMethod(unittest.TestCase):
    def test_Inheritance(self):
        self.assertTrue(issubclass(Method, XmlModel))

    def test_Dump(self):
        obj = Method(
            name="Method 1",
            id="method1",
        )
        xml = obj.dump_xml()

        self.assertIsNotNone(xml)
        self.assertEqual(xml.tag, "Method")
        self.assertEqual(xml.attrib["name"], "Method 1")
        self.assertEqual(xml.attrib["id"], "method1")

    def test_Load(self):
        xml = Element("Method")
        xml.attrib["name"] = "Method 1"
        xml.attrib["id"] = "method1"

        obj = Method.load_xml(xml)
        self.assertIsInstance(obj, Method)
        self.assertEqual(obj.name, "Method 1")
        self.assertEqual(obj.id, "method1")
        self.assertIsNone(obj.author)
        self.assertIsNone(obj.device)
        self.assertIsNone(obj.software)
        self.assertIsNone(obj.category)
