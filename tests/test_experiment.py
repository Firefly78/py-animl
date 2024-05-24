import unittest
from xml.etree import ElementTree

from animl2.core import XmlModel
from animl2.models.experiment import ExperimentStep, ExperimentStepSet


class TestExperimentStep(unittest.TestCase):
    def setUp(self):
        self.example_step = ExperimentStep(
            experimentStepID="c1234",
            name="Step 1",
            comment="This is a comment",
            id="a1234",
            sourceDataLocation="http://example.com",
            templateUsed="http://example.com",
        )

    def test_Inheritance(self):
        self.assertIsInstance(self.example_step, XmlModel)

    def test_Dump(self):
        xml = self.example_step.dump_xml()
        self.assertEqual(xml.tag, "ExperimentStep")
        self.assertEqual(xml.attrib["experimentStepID"], "c1234")
        self.assertEqual(xml.attrib["name"], "Step 1")
        self.assertEqual(xml.attrib["comment"], "This is a comment")
        self.assertEqual(xml.attrib["id"], "a1234")
        self.assertEqual(xml.attrib["sourceDataLocation"], "http://example.com")
        self.assertEqual(xml.attrib["templateUsed"], "http://example.com")

    def test_Load(self):
        txt = """
        <ExperimentStep experimentStepID="c1234" name="Step 1" comment="This is a comment"
            id="a1234" sourceDataLocation="http://example.com" templateUsed="http://example.com"/>
        """
        s = ExperimentStep.load_xml(ElementTree.fromstring(txt))
        self.assertIsInstance(s, ExperimentStep)
        self.assertEqual(s.experimentStepID, "c1234")
        self.assertEqual(s.name, "Step 1")
        self.assertEqual(s.comment, "This is a comment")
        self.assertEqual(s.id, "a1234")
        self.assertEqual(s.sourceDataLocation, "http://example.com")
        self.assertEqual(s.templateUsed, "http://example.com")


class TestExperimentStepSet(unittest.TestCase):
    def test_Inheritance(self):
        self.assertIsInstance(ExperimentStepSet(), XmlModel)
