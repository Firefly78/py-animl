import unittest

from simple_animl.core import XmlModel
from simple_animl.models.doc import (
    VERSION,
    XMLNS,
    XMLNS_XSI,
    XSI_SCHEMALOCATION,
    AnIMLDoc,
)


class TestDoc(unittest.TestCase):
    def test_Inheritance(self):
        doc = AnIMLDoc()
        self.assertIsInstance(doc, XmlModel)

    def test_Create(self):
        doc = AnIMLDoc()
        self.assertIsNone(doc.sample_set)

    def test_Dump(self):
        doc = AnIMLDoc()
        xml = doc.dump_xml()
        """
        xml = <AnIML version="0.90"
            xmlns="urn:org:astm:animl:schema:core:draft:0.90"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xsi:schemaLocation="urn:org:astm:animl:schema:core:draft:0.90 http://schemas.animl.org/current/animl-core.xsd"/>
        """
        self.assertEqual(xml.tag, "AnIML")
        self.assertIn("version", xml.attrib)
        self.assertEqual(xml.attrib["version"], VERSION)
        self.assertIn("xmlns", xml.attrib)
        self.assertEqual(xml.attrib["xmlns"], XMLNS)
        self.assertIn("xmlns:xsi", xml.attrib)
        self.assertEqual(xml.attrib["xmlns:xsi"], XMLNS_XSI)
        self.assertIn("xsi:schemaLocation", xml.attrib)
        self.assertEqual(xml.attrib["xsi:schemaLocation"], XSI_SCHEMALOCATION)

    def test_Load(self):
        txt = '<?xml version="1.0" encoding="UTF-8"?><AnIML version="0.90"/>'
        doc = AnIMLDoc.loads(txt)
        self.assertIsInstance(doc, AnIMLDoc)
        self.assertIsNone(doc.sample_set)
