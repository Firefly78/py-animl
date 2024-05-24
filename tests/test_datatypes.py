import unittest
from datetime import datetime

from animl2.core.base import XmlModel
from animl2.models.data_type import (
    BooleanType,
    DateTimeType,
    DoubleType,
    EmbeddedXmlType,
    FloatType,
    IntType,
    LongType,
    PNGType,
    StringType,
    SVGType,
)


class TestTypes(unittest.TestCase):
    def test_Boolean(self):
        self.assertIsInstance(BooleanType(value=True), XmlModel)
        xml = BooleanType(value=True).dump_xml()
        self.assertEqual(xml.text, "true")
        self.assertEqual(xml.tag, "Boolean")

    def test_Double(self):
        self.assertIsInstance(DoubleType(value=1.0), XmlModel)
        xml = DoubleType(value=1.0).dump_xml()
        self.assertEqual(xml.text, "1.0")
        self.assertEqual(xml.tag, "D")

    def test_DateTime(self):
        self.assertIsInstance(DateTimeType(value=datetime(2021, 1, 1)), XmlModel)
        xml = DateTimeType(value=datetime(2021, 1, 1)).dump_xml()
        self.assertEqual(xml.text, "2021-01-01T00:00:00")
        self.assertEqual(xml.tag, "DateTime")

    def test_EmbeddedXml(self):
        self.assertIsInstance(EmbeddedXmlType(value="<xml></xml>"), XmlModel)
        xml = EmbeddedXmlType(value="<xml></xml>").dump_xml()
        self.assertEqual(xml.text, "<xml></xml>")
        self.assertEqual(xml.tag, "EmbeddedXML")

    def test_Float(self):
        self.assertIsInstance(FloatType(value=1.0), XmlModel)
        xml = FloatType(value=1.0).dump_xml()
        self.assertEqual(xml.text, "1.0")
        self.assertEqual(xml.tag, "F")

    def test_Int(self):
        self.assertIsInstance(IntType(value=1), XmlModel)
        xml = IntType(value=1).dump_xml()
        self.assertEqual(xml.text, "1")
        self.assertEqual(xml.tag, "I")

    def test_Long(self):
        self.assertIsInstance(LongType(value=1), XmlModel)
        xml = LongType(value=1).dump_xml()
        self.assertEqual(xml.text, "1")
        self.assertEqual(xml.tag, "L")

    def test_PNG(self):
        self.assertIsInstance(PNGType(), XmlModel)
        xml = PNGType().dump_xml()
        self.assertEqual(xml.text, None)
        self.assertEqual(xml.tag, "PNG")

    def test_String(self):
        self.assertIsInstance(StringType(value="string"), XmlModel)
        xml = StringType(value="string").dump_xml()
        self.assertEqual(xml.text, "string")
        self.assertEqual(xml.tag, "S")

    def test_SVG(self):
        self.assertIsInstance(SVGType(value="<svg></svg>"), XmlModel)
        xml = SVGType(value="<svg></svg>").dump_xml()
        self.assertEqual(xml.text, "<svg></svg>")
        self.assertEqual(xml.tag, "SVG")
