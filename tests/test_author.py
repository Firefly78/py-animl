import unittest
from xml.etree.ElementTree import Element

from animl2.core import XmlModel
from animl2.models import Name
from animl2.models.author import Author, UserType


class TestAuthor(unittest.TestCase):
    def test_Inheritance(self):
        self.assertTrue(issubclass(Author, XmlModel))

    def test_Dump(self):
        obj = Author(userType=UserType.Human, name=Name(value="John Doe"))
        xml = obj.dump_xml()

        self.assertIsNotNone(xml)
        self.assertEqual(xml.tag, "Author")
        self.assertEqual(xml.attrib["userType"], "human")

        name = xml.find("Name")
        self.assertIsNotNone(name)

    def test_Load(self):
        xml = Element("Author", userType="human")
        name = Element("Name")
        name.text = "John Doe"
        xml.append(name)

        obj = Author.load_xml(xml)
        self.assertIsInstance(obj, Author)
        self.assertEqual(obj.userType, UserType.Human)
        self.assertIsInstance(obj.name, Name)
