import unittest
from xml.etree.ElementTree import Element

from animl2.core import XmlModel
from animl2.models.common import Manufacturer, Name
from animl2.models.software import OperatingSystem, Software, Version
from helpers import make_element


class Test_OperatingSystem(unittest.TestCase):
    def test_Inheritance(self):
        self.assertTrue(issubclass(OperatingSystem, XmlModel))

    def test_Dump(self):
        obj = OperatingSystem(value="Blingux :)")
        xml = obj.dump_xml()

        self.assertIsNotNone(xml)
        self.assertEqual(xml.tag, "OperatingSystem")
        self.assertEqual(xml.text, "Blingux :)")

    def test_Load(self):
        xml = Element("OperatingSystem")
        xml.text = "Blingux :)"

        obj = OperatingSystem.load_xml(xml)
        self.assertIsInstance(obj, OperatingSystem)
        self.assertEqual(obj.value, "Blingux :)")


class Test_Version(unittest.TestCase):
    def test_Inheritance(self):
        self.assertTrue(issubclass(Version, XmlModel))

    def test_Dump(self):
        obj = Version(value="1.0.0")
        xml = obj.dump_xml()

        self.assertIsNotNone(xml)
        self.assertEqual(xml.tag, "Version")
        self.assertEqual(xml.text, "1.0.0")

    def test_Load(self):
        xml = Element("Version")
        xml.text = "1.0.0"

        obj = Version.load_xml(xml)
        self.assertIsInstance(obj, Version)
        self.assertEqual(obj.value, "1.0.0")


class Test_Software(unittest.TestCase):
    def test_Inheritance(self):
        self.assertTrue(issubclass(Software, XmlModel))

    def test_Dump(self):
        obj = Software(
            name=Name("Software 1"),
            manufacturer=Manufacturer("ACME Corp"),
            version=Version("1.0.0"),
            operating_system=OperatingSystem("Blingux :)"),
        )
        xml = obj.dump_xml()

        self.assertIsNotNone(xml)
        self.assertEqual(xml.tag, "Software")
        self.assertEqual(xml.find("Name").text, "Software 1")
        self.assertEqual(xml.find("Manufacturer").text, "ACME Corp")
        self.assertEqual(xml.find("Version").text, "1.0.0")
        self.assertEqual(xml.find("OperatingSystem").text, "Blingux :)")

    def test_Load(self):
        xml = Element("Software")
        xml.append(make_element("Name", text="Software 1"))
        xml.append(make_element("Manufacturer", text="ACME Corp"))
        xml.append(make_element("Version", text="1.0.0"))
        xml.append(make_element("OperatingSystem", text="Blingux :)"))

        obj = Software.load_xml(xml)
        self.assertIsInstance(obj, Software)
        self.assertEqual(obj.name.value, "Software 1")
        self.assertEqual(obj.manufacturer.value, "ACME Corp")
        self.assertEqual(obj.version.value, "1.0.0")
        self.assertEqual(obj.operating_system.value, "Blingux :)")
