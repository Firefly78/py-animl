import unittest
from xml.etree import ElementTree

from simple_animl import AnIMLDoc
from simple_animl.models.core import XmlModel
from simple_animl.models.sample import Sample, SampleSet


class TestSample(unittest.TestCase):
    def test_Inheritance(self):
        s = Sample(name="Sample 1", sampleID="1234")
        self.assertIsInstance(s, XmlModel)

    def test_Create(self):
        doc = AnIMLDoc()
        s1 = Sample(name="Sample 1", sampleID="1234")
        s2 = Sample(name="Sample 2", sampleID="5678")
        doc.add(s1)
        doc.add(s2)
        self.assertIn(s1, doc.sample_set.samples)
        self.assertIn(s2, doc.sample_set.samples)

    def test_SetID(self):
        doc = AnIMLDoc()
        doc.sample_set = SampleSet(id="Hello")
        doc.add(Sample(name="Sample 1", sampleID="1234"))

    def test_Dump(self):
        doc = AnIMLDoc()
        doc.add(Sample(name="Sample 1", sampleID="1234"))
        doc.add(Sample(name="Sample 1", sampleID="1234"))
        doc.add(Sample(name="Sample 1", sampleID="1234"))
        xml = doc.dump_xml()
        """
        xml = <AnIML version="0.90"
            xmlns="urn:org:astm:animl:schema:core:draft:0.90"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xsi:schemaLocation="urn:org:astm:animl:schema:core:draft:0.90 http://schemas.animl.org/current/animl-core.xsd">
        </AnIML>
        """

        print(ElementTree.tostring(xml, encoding="unicode"))
