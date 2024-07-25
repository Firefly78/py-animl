import unittest
from xml.etree.ElementTree import Element

from animl2.core import XmlModel
from animl2.models.technique import Extension, Technique


class Test_Extension(unittest.TestCase):
    def test_Inheritance(self):
        self.assertTrue(issubclass(Extension, XmlModel))

    def test_Dump(self):
        obj = Extension(
            name="Extension 1",
            uri="http://example.com/ext1",
            sha256="1234567890abcdef",
        )
        xml = obj.dump_xml()

        self.assertIsNotNone(xml)
        self.assertEqual(xml.tag, "Extension")
        self.assertEqual(xml.attrib["name"], "Extension 1")
        self.assertEqual(xml.attrib["uri"], "http://example.com/ext1")
        self.assertEqual(xml.attrib["sha256"], "1234567890abcdef")

    def test_Load(self):
        xml = Element("Extension")
        xml.attrib["name"] = "Extension 1"
        xml.attrib["uri"] = "http://example.com/ext1"
        xml.attrib["sha256"] = "1234567890abcdef"

        obj = Extension.load_xml(xml)
        self.assertIsInstance(obj, Extension)
        self.assertEqual(obj.name, "Extension 1")
        self.assertEqual(obj.uri, "http://example.com/ext1")
        self.assertEqual(obj.sha256, "1234567890abcdef")


class Test_Technique(unittest.TestCase):
    def test_Inheritance(self):
        self.assertTrue(issubclass(Technique, XmlModel))

    def test_Dump(self):
        obj = Technique(
            name="Technique 1",
            uri="http://example.com/tech1",
            id="technique1",
            sha256="1234567890abcdef",
        )

        obj.append(Extension(name="Extension 1", uri="http://example.com/ext1"))

        xml = obj.dump_xml()

        self.assertIsNotNone(xml)
        self.assertEqual(xml.tag, "Technique")
        self.assertEqual(xml.attrib["name"], "Technique 1")
        self.assertEqual(xml.attrib["uri"], "http://example.com/tech1")
        self.assertEqual(xml.attrib["id"], "technique1")
        self.assertEqual(xml.attrib["sha256"], "1234567890abcdef")

        ext = xml.find("Extension")
        self.assertIsNotNone(ext)
        self.assertEqual(ext.attrib["name"], "Extension 1")
        self.assertEqual(ext.attrib["uri"], "http://example.com/ext1")

    def test_Load(self):
        xml = Element("Technique")
        xml.attrib["name"] = "Technique 1"
        xml.attrib["id"] = "technique1"
        xml.attrib["uri"] = "http://example.com/tech1"
        xml.attrib["sha256"] = "1234567890abcdef"

        ext = Element("Extension")
        ext.attrib["name"] = "Extension 1"
        ext.attrib["uri"] = "http://example.com/ext1"

        xml.append(ext)

        obj = Technique.load_xml(xml)
        self.assertIsInstance(obj, Technique)
        self.assertEqual(obj.name, "Technique 1")
        self.assertEqual(obj.id, "technique1")
        self.assertEqual(obj.uri, "http://example.com/tech1")
        self.assertEqual(obj.sha256, "1234567890abcdef")

        self.assertEqual(len(obj.extensions), 1)
        self.assertIsInstance(obj.extensions[0], Extension)
