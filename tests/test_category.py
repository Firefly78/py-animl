import unittest
from xml.etree import ElementTree

from simple_animl import Category, Sample
from simple_animl.core.base import XmlModel


class TestCategory(unittest.TestCase):
    def test_Inheritance(self):
        c = Category(name="Category 1")
        self.assertIsInstance(c, XmlModel)

    def test_Dump(self):
        sample = Sample(name="Sample 1", sampleID="1234")
        sample.category = Category(name="Category 1", id="1234")
        xml = sample.dump_xml()

        cat = xml.find("Category")
        self.assertIsNotNone(cat)

        self.assertEqual(cat.tag, "Category")
        self.assertEqual(cat.attrib["name"], "Category 1")
        self.assertEqual(cat.attrib["id"], "1234")

    def test_Load(self):
        txt = """
        <Sample name="Sample 1" sampleID="12345">
            <Category name="Category 1" id="1234"/>
        </Sample>
        """
        sample = Sample.load_xml(ElementTree.fromstring(txt))
        self.assertIsInstance(sample.category, Category)
        self.assertEqual(sample.category.name, "Category 1")
        self.assertEqual(sample.category.id, "1234")
