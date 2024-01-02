import unittest
from xml.etree import ElementTree

from simple_animl import AnIMLDoc
from simple_animl.core import XmlModel
from simple_animl.models.sample import Sample, SampleSet


class TestSample(unittest.TestCase):
    def test_Inheritance(self):
        s = Sample(name="Sample 1", sampleID="1234")
        self.assertIsInstance(s, XmlModel)

    def test_Create(self):
        doc = AnIMLDoc()
        s1 = Sample(name="Sample 1", sampleID="1234")
        s2 = Sample(name="Sample 2", sampleID="5678")
        doc.sample_set = SampleSet()
        doc.sample_set.add(s1)
        doc.sample_set.add(s2)
        self.assertIn(s1, doc.sample_set.samples)
        self.assertIn(s2, doc.sample_set.samples)

    def test_SetID(self):
        doc = AnIMLDoc()
        doc.sample_set = SampleSet(id="Hello")
        doc.sample_set.add(Sample(name="Sample 1", sampleID="1234"))

    def test_Dump(self):
        doc = AnIMLDoc()
        doc.sample_set = SampleSet()
        doc.sample_set.add(Sample(name="Sample 1", sampleID="1"))
        doc.sample_set.add(Sample(name="Sample 2", sampleID="2"))
        doc.sample_set.add(Sample(name="Sample 3", sampleID="3"))
        xml = doc.dump_xml()
        """
        xml = <AnIML version="0.90"
            xmlns="urn:org:astm:animl:schema:core:draft:0.90"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xsi:schemaLocation="urn:org:astm:animl:schema:core:draft:0.90 http://schemas.animl.org/current/animl-core.xsd">
            <SampleSet>
                <Sample name="Sample 1" sampleID="1"/>
                <Sample name="Sample 2" sampleID="2"/>
                <Sample name="Sample 3" sampleID="3"/>
            </SampleSet>
        </AnIML>
        """
        set = xml.find("SampleSet")
        self.assertEqual(set.tag, "SampleSet")
        samples = [s for s in set]
        for sample in samples:
            self.assertEqual(sample.tag, "Sample")
            self.assertIn("name", sample.attrib)
            self.assertIn("sampleID", sample.attrib)

        self.assertEqual(samples[0].attrib["name"], "Sample 1")
        self.assertEqual(samples[1].attrib["name"], "Sample 2")
        self.assertEqual(samples[2].attrib["name"], "Sample 3")

        self.assertEqual(samples[0].attrib["sampleID"], "1")
        self.assertEqual(samples[1].attrib["sampleID"], "2")
        self.assertEqual(samples[2].attrib["sampleID"], "3")

    def test_Load(self):
        txt = """<?xml version="1.0" encoding="UTF-8"?>
        <AnIML version="0.90">
            <SampleSet>
                <Sample name="Sample 1" sampleID="1"/>
                <Sample name="Sample 2" sampleID="2"/>
                <Sample name="Sample 3" sampleID="3"/>
            </SampleSet>
        </AnIML>"""

        doc = AnIMLDoc.loads(txt)
        samples = doc.sample_set.samples
        self.assertEqual(len(samples), 3)
        self.assertEqual(samples[0].name, "Sample 1")
        self.assertEqual(samples[1].name, "Sample 2")
        self.assertEqual(samples[2].name, "Sample 3")
        self.assertEqual(samples[0].sampleID, "1")
        self.assertEqual(samples[1].sampleID, "2")
        self.assertEqual(samples[2].sampleID, "3")
