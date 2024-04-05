import unittest
from enum import Enum
from xml.etree import ElementTree

from simple_animl.core import XmlModel
from simple_animl.core.annotations import Annotation
from simple_animl.models.base import AnIMLDocBase
from simple_animl.models.unit import SIUnit, Unit, UnitText


class TestSIUnit(unittest.TestCase):
    def test_Inheritance(self):
        s = SIUnit(unit=UnitText.Meter)
        self.assertIsInstance(s, XmlModel)

    def test_Create(self):
        kwargs = {
            "exponent": "1",
            "factor": "1.0",
            "offset": "5",
            "unit": UnitText.Candela,
        }

        s = SIUnit(**kwargs)
        self.assertEqual(s.exponent, kwargs["exponent"])
        self.assertEqual(s.factor, kwargs["factor"])
        self.assertEqual(s.offset, kwargs["offset"])
        self.assertEqual(s.unit, kwargs["unit"])

    def test_Dump(self):
        kwargs = {
            "exponent": "1",
            "factor": "1.0",
            "offset": "5",
            "unit": UnitText.Candela,
        }

        s = SIUnit(**kwargs)
        xml = s.dump_xml()
        self.assertEqual(xml.tag, "SIUnit")
        self.assertEqual(xml.attrib["exponent"], kwargs["exponent"])
        self.assertEqual(xml.attrib["factor"], kwargs["factor"])
        self.assertEqual(xml.attrib["offset"], kwargs["offset"])
        self.assertEqual(xml.text, kwargs["unit"].value)

    def test_Load(self):
        txt = """<SIUnit exponent="1" factor="1.0" offset="5">cd</SIUnit>"""
        u = SIUnit.load_xml(ElementTree.fromstring(txt))
        self.assertEqual(u.exponent, "1")
        self.assertEqual(u.factor, "1.0")
        self.assertEqual(u.offset, "5")
        self.assertEqual(u.unit, UnitText.Candela)


class TestUnits(unittest.TestCase):
    def test_Inheritance(self):
        s = Unit(label="test_label")
        self.assertIsInstance(s, XmlModel)

    def test_Create(self):
        kwargs = {
            "label": "test_label",
            "quantity": "test_quantity",
            "siunits": [SIUnit(unit=UnitText.Meter)],
        }

        s = Unit(**kwargs)
        self.assertEqual(s.label, kwargs["label"])
        self.assertEqual(s.quantity, kwargs["quantity"])
        self.assertEqual(s.siunits, kwargs["siunits"])

    def test_Dump(self):
        kwargs = {
            "label": "test_label",
            "quantity": "test_quantity",
            "siunits": [
                SIUnit(unit=UnitText.Meter),
                SIUnit(unit=UnitText.Kg),
            ],
        }

        s = Unit(**kwargs)
        xml = s.dump_xml()
        self.assertEqual(xml.tag, "Unit")
        self.assertEqual(xml.attrib["label"], kwargs["label"])
        self.assertEqual(xml.attrib["quantity"], kwargs["quantity"])
        self.assertEqual(len(xml.findall("SIUnit")), 2)

    def test_Load(self):
        txt = """<Unit label="test_label" quantity="test_quantity">
            <SIUnit>cd</SIUnit>
        </Unit>"""
        u = Unit.load_xml(ElementTree.fromstring(txt))
        self.assertEqual(u.label, "test_label")
        self.assertEqual(u.quantity, "test_quantity")
        self.assertEqual(len(u.siunits), 1)
        self.assertEqual(u.siunits[0].exponent, None)
        self.assertEqual(u.siunits[0].factor, None)
        self.assertEqual(u.siunits[0].offset, None)
        self.assertEqual(u.siunits[0].unit, UnitText.Candela)


class TestUnitText(unittest.TestCase):
    def test_Inheritance(self):
        self.assertTrue(issubclass(UnitText, Enum))
        self.assertTrue(issubclass(UnitText, str))

    def test_Register(self):
        self.assertIn(UnitText, AnIMLDocBase.get_registered_types().values())
