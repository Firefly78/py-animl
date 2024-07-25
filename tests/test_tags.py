import unittest
from xml.etree.ElementTree import Element

from animl2.core import XmlModel
from animl2.models.tags import Tag, TagSet


class Test_Tag(unittest.TestCase):
    def test_Inheritance(self):
        self.assertTrue(issubclass(Tag, XmlModel))

    def test_Dump(self):
        obj = Tag(
            name="Tag 1",
            value="tag1",
        )
        xml = obj.dump_xml()

        self.assertIsNotNone(xml)
        self.assertEqual(xml.tag, "Tag")
        self.assertEqual(xml.attrib["name"], "Tag 1")
        self.assertEqual(xml.attrib["value"], "tag1")

    def test_Load(self):
        xml = Element("Tag")
        xml.attrib["name"] = "Tag 1"
        xml.attrib["value"] = "tag1"

        obj = Tag.load_xml(xml)
        self.assertIsInstance(obj, Tag)
        self.assertEqual(obj.name, "Tag 1")
        self.assertEqual(obj.value, "tag1")


class Test_TagSet(unittest.TestCase):
    def test_Inheritance(self):
        self.assertTrue(issubclass(TagSet, XmlModel))

    def test_Dump(self):
        obj = TagSet(
            tags=[
                Tag(name="Tag 1", value="tag1"),
            ],
        )

        obj.append(Tag(name="Tag 2", value="tag2"))
        xml = obj.dump_xml()

        self.assertIsNotNone(xml)
        self.assertEqual(xml.tag, "TagSet")

        tags = xml.findall("Tag")
        self.assertEqual(len(tags), 2)

        self.assertEqual(tags[0].attrib["name"], "Tag 1")
        self.assertEqual(tags[0].attrib["value"], "tag1")

        self.assertEqual(tags[1].attrib["name"], "Tag 2")
        self.assertEqual(tags[1].attrib["value"], "tag2")

    def test_Load(self):
        xml = Element("TagSet")
        xml.append(Element("Tag", attrib={"name": "Tag 1", "value": "tag1"}))
        xml.append(Element("Tag", attrib={"name": "Tag 2", "value": "tag2"}))

        obj = TagSet.load_xml(xml)
        self.assertIsInstance(obj, TagSet)

        self.assertEqual(len(obj.tags), 2)
        self.assertIsInstance(obj.tags[0], Tag)
        self.assertEqual(obj.tags[0].name, "Tag 1")
        self.assertEqual(obj.tags[0].value, "tag1")
        self.assertIsInstance(obj.tags[1], Tag)
        self.assertEqual(obj.tags[1].name, "Tag 2")
        self.assertEqual(obj.tags[1].value, "tag2")
