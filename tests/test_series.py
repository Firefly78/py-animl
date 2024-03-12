import unittest
from xml.etree import ElementTree

from simple_animl.core.base import XmlModel
from simple_animl.models.series import (
    Dependency,
    ParameterTypes,
    PlotScale,
    Series,
    SeriesSet,
)
from simple_animl.models.unit import SIUnit, Unit


class TestSeriesSet(unittest.TestCase):
    def setUp(self):
        self.example_series = Series(
            name="Series 1",
            dependency=Dependency.Independent,
            id="c1234",
            PlotScale=PlotScale.Linear,
            seriesID="b1234",
            seriesType=ParameterTypes.Int32,
            visible=True,
            valuesets=[],
            unit=Unit(label="m", quantity="m", siunits=[SIUnit()]),
        )
        self.example_set = SeriesSet(
            name="SeriesSet1", length=10, id="a1234", series=[self.example_series]
        )

    def test_Inheritance(self):
        self.assertIsInstance(self.example_set, XmlModel)

    def test_Dump(self):
        xml = self.example_set.dump_xml()
        self.assertEqual(xml.tag, "SeriesSet")
        self.assertEqual(xml.attrib["name"], "SeriesSet1")
        self.assertEqual(xml.attrib["length"], "10")
        self.assertEqual(xml.attrib["id"], "a1234")
        self.assertEqual(len(xml.findall("Series")), 1)

    def test_Load(self):
        txt = """
        <SeriesSet name="MySeriesSet" length="5" id="A">
            <Series name="MySeries" dependency="independent" seriesID="" seriesType="Boolean"
                id="A0" plotScale="none" visible="true">
                <EncodedValueSet>001</EncodedValueSet>
            </Series>
        </SeriesSet>
        """
        s = SeriesSet.load_xml(ElementTree.fromstring(txt))
        self.assertIsInstance(s, SeriesSet)
        self.assertEqual(s.name, "MySeriesSet")
        self.assertEqual(s.length, 5)
        self.assertEqual(s.id, "A")
        self.assertEqual(len(s.series), 1)
        self.assertIsInstance(s.series[0], Series)
        self.assertEqual(s.series[0].name, "MySeries")


class TestSeries(unittest.TestCase):
    def setUp(self):
        self.example = Series(
            name="Series 1",
            dependency=Dependency.Independent,
            id="c1234",
            plotScale=PlotScale.Linear,
            seriesID="b1234",
            seriesType=ParameterTypes.Int32,
            visible=True,
            valuesets=[],
            unit=Unit(label="m", quantity="m", siunits=[SIUnit()]),
        )

    def test_Inheritance(self):
        self.assertIsInstance(self.example, XmlModel)

    def test_Dump(self):
        xml = self.example.dump_xml()
        self.assertEqual(xml.tag, "Series")
        self.assertEqual(xml.attrib["name"], "Series 1")
        self.assertEqual(xml.attrib["dependency"], "independent")
        self.assertEqual(xml.attrib["id"], "c1234")
        self.assertEqual(xml.attrib["plotScale"], "linear")
        self.assertEqual(xml.attrib["seriesID"], "b1234")
        self.assertEqual(xml.attrib["seriesType"], "Int32")
        self.assertEqual(xml.attrib["visible"], "true")
        self.assertEqual(len(xml.findall("Unit")), 1)

    def test_Load(self):
        txt = """
        <Series name="MySeries" dependency="independent" seriesID="" seriesType="Boolean"
            id="A0" plotScale="none" visible="true">
            <EncodedValueSet></EncodedValueSet>
        </Series>
        """
        s = Series.load_xml(ElementTree.fromstring(txt))
        self.assertIsInstance(s, Series)
        self.assertEqual(s.name, "MySeries")
        self.assertEqual(s.dependency, Dependency.Independent)
        self.assertEqual(s.id, "A0")
        self.assertEqual(s.plotScale, PlotScale.none)
