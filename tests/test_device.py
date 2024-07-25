import unittest

from helpers import make_element

from animl2.core import XmlModel
from animl2.models.common import Manufacturer, Name
from animl2.models.device import Device, DeviceIdentifier, FirmwareVersion, SerialNumber


class TestDevice(unittest.TestCase):
    def test_Inheritance(self):
        self.assertTrue(issubclass(Device, XmlModel))
        self.assertTrue(issubclass(DeviceIdentifier, XmlModel))
        self.assertTrue(issubclass(FirmwareVersion, XmlModel))
        self.assertTrue(issubclass(SerialNumber, XmlModel))

    def test_Dump(self):
        obj = Device(
            identifier=DeviceIdentifier(value="Device 1"),
            manufacturer=Manufacturer(value="ACME Corp"),
            name=Name(value="Device"),
            firmware=FirmwareVersion(value="1.0"),
            serialNumber=SerialNumber(value="1234"),
        )
        xml = obj.dump_xml()

        self.assertIsNotNone(xml)
        self.assertEqual(xml.tag, "Device")

        self.assertIsNotNone(xml.find("DeviceIdentifier"))
        self.assertEqual(xml.find("DeviceIdentifier").text, "Device 1")

        self.assertIsNotNone(xml.find("Manufacturer"))
        self.assertEqual(xml.find("Manufacturer").text, "ACME Corp")

        self.assertIsNotNone(xml.find("Name"))
        self.assertEqual(xml.find("Name").text, "Device")

        self.assertIsNotNone(xml.find("FirmwareVersion"))
        self.assertEqual(xml.find("FirmwareVersion").text, "1.0")

        self.assertIsNotNone(xml.find("SerialNumber"))
        self.assertEqual(xml.find("SerialNumber").text, "1234")

    def test_Load(self):
        xml = make_element(
            "Device",
            children=[
                make_element("DeviceIdentifier", text="Device 1"),
                make_element("Manufacturer", text="ACME Corp"),
                make_element("Name", text="Device"),
                make_element("FirmwareVersion", text="1.0"),
                make_element("SerialNumber", text="1234"),
            ],
        )

        obj = Device.load_xml(xml)
        self.assertIsInstance(obj, Device)
        self.assertIsInstance(obj.identifier, DeviceIdentifier)
        self.assertEqual(obj.identifier.value, "Device 1")
        self.assertIsInstance(obj.manufacturer, Manufacturer)
        self.assertEqual(obj.manufacturer.value, "ACME Corp")
        self.assertIsInstance(obj.name, Name)
        self.assertEqual(obj.name.value, "Device")
        self.assertIsInstance(obj.firmware, FirmwareVersion)
        self.assertEqual(obj.firmware.value, "1.0")
        self.assertIsInstance(obj.serialNumber, SerialNumber)
        self.assertEqual(obj.serialNumber.value, "1234")
