import unittest
from xml.etree import ElementTree

from simple_animl.core import XmlModel
from simple_animl.models.data_type import DoubleType, FloatType, IntType, LongType
from simple_animl.models.valuesets import AutoIncrementedValueSet as AIVS
from simple_animl.models.valuesets import EncodedValueSet as EVS
from simple_animl.models.valuesets import IndividualValueSet as IVS


class TestAutoIncrSets(unittest.TestCase):
    def test_Inheritance(self):
        s = AIVS(startValue=IntType(value=1), increment=IntType(value=1))
        self.assertIsInstance(s, XmlModel)

    def test_Dump(self):
        s = AIVS(
            startValue=FloatType(value=1),
            increment=IntType(value=1),
            startIndex=0,
            endIndex=10,
        )
        xml = s.dump_xml()

        self.assertEqual(xml.tag, AIVS.tag)

        self.assertEqual(xml.attrib["startIndex"], "0")
        self.assertEqual(xml.attrib["endIndex"], "10")

        self.assertIsNotNone(xml.find(FloatType.tag))
        self.assertIsNotNone(xml.find(IntType.tag))

    def test_Load(self):
        txt = """
        <AutoIncrementedValueSet startIndex="0" endIndex="10">
            <I>5</I>
            <I>1</I>
        </AutoIncrementedValueSet>
        """
        s = AIVS.load_xml(ElementTree.fromstring(txt))

        self.assertIsInstance(s, AIVS)
        self.assertEqual(s.startIndex, 0)
        self.assertEqual(s.endIndex, 10)
        self.assertIsInstance(s.startValue, IntType)
        self.assertEqual(s.startValue.value, 5)
        self.assertIsInstance(s.increment, IntType)
        self.assertEqual(s.increment.value, 1)


class TestEncodedValueSet(unittest.TestCase):
    def test_Inheritance(self):
        s = EVS(value=b"1234")
        self.assertIsInstance(s, XmlModel)

    def test_Dump(self):
        s = EVS(
            value=b"1234",
            startIndex=0,
            endIndex=10,
        )
        xml = s.dump_xml()

        self.assertEqual(xml.tag, EVS.tag)

        self.assertEqual(xml.attrib["startIndex"], "0")
        self.assertEqual(xml.attrib["endIndex"], "10")

        self.assertEqual(xml.text, b"1234".decode("ascii"))

    def test_Load(self):
        txt = """
        <EncodedValueSet startIndex="0" endIndex="10">1234</EncodedValueSet>
        """
        s = EVS.load_xml(ElementTree.fromstring(txt))

        self.assertIsInstance(s, EVS)
        self.assertEqual(s.startIndex, 0)
        self.assertEqual(s.endIndex, 10)
        self.assertEqual(s.value, b"1234")


class TestIndividualValueSet(unittest.TestCase):
    def test_Inheritance(self):
        s = IVS(values=[IntType(value=1), IntType(value=2)])
        self.assertIsInstance(s, XmlModel)

    def test_Dump(self):
        s = IVS(
            values=[IntType(value=1), IntType(value=2)],
            startIndex=0,
            endIndex=10,
        )
        xml = s.dump_xml()

        self.assertEqual(xml.tag, IVS.tag)

        self.assertEqual(xml.attrib["startIndex"], "0")
        self.assertEqual(xml.attrib["endIndex"], "10")

        m = xml.findall(IntType.tag)
        self.assertEqual(len(m), 2)
        self.assertEqual(m[0].text, "1")
        self.assertEqual(m[1].text, "2")

    def test_Load(self):
        txt = """
        <IndividualValueSet startIndex="0" endIndex="10">
            <I>1</I>
            <I>2</I>
        </IndividualValueSet>
        """
        s = IVS.load_xml(ElementTree.fromstring(txt))

        self.assertIsInstance(s, IVS)
        self.assertEqual(s.startIndex, 0)
        self.assertEqual(s.endIndex, 10)
        self.assertEqual(len(s.values), 2)
