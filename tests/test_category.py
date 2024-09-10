import unittest
from xml.etree import ElementTree

from animl2.core.base import XmlModel
from animl2.models.category import Category
from animl2.models.sample import Sample


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
        self.assertIsInstance(sample.category[0], Category)
        self.assertEqual(sample.category[0].name, "Category 1")
        self.assertEqual(sample.category[0].id, "1234")
