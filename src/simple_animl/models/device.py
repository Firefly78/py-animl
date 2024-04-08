from typing import Optional

from ..core import Field, XmlModel
from .base import AnIMLDocBase
from .common import Manufacturer, Name


class DeviceIdentifier(XmlModel, regclass=AnIMLDocBase):
    """
    Unique name or identifier of the device.

    Text:
        value (str): Identifier value
    """

    # Text
    value: str = Field.Attribute()


class Firmware(XmlModel, regclass=AnIMLDocBase):
    """
    Version identifier of firmware release.

    Text:
        value (str): Firmware value
    """

    # Text
    value: str = Field.Text()


class SerialNumber(XmlModel, regclass=AnIMLDocBase):
    """
    Unique serial number of device

    Text:
        value (str): Serial number value
    """

    # Text
    value: str = Field.Text()


class Device(XmlModel, regclass=AnIMLDocBase):
    """
    Device used to perform experiment.

    Children:
        firmware (Firmware): Version identifier of firmware release.
        identifier (DeviceIdentifier): Unique name or identifier of the device.
        manufacturer (Manufacturer): Company name.
        name (Name): Common name.
        serialNumber (SerialNumber): Unique serial number of device

    """

    # Children
    firmware: Optional[Firmware] = Field.Child()
    identifier: DeviceIdentifier = Field.Child()
    manufacturer: Manufacturer = Field.Child()
    name: Name = Field.Child()
    serialNumber: Optional[SerialNumber] = Field.Child()
