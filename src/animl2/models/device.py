from dataclasses import dataclass
from typing import Annotated, Optional

from ..core import ATTRIB, CHILD, TEXT, XmlModel
from .base import AnIMLDocBase
from .common import Manufacturer, Name


@dataclass
class DeviceIdentifier(XmlModel, regclass=AnIMLDocBase):
    """
    Unique name or identifier of the device.

    Text:
        value (str): Identifier value
    """

    # Text
    value: Annotated[str, ATTRIB]


@dataclass
class FirmwareVersion(XmlModel, regclass=AnIMLDocBase):
    """
    Version identifier of firmware release.

    Text:
        value (str): Firmware version value
    """

    # Text
    value: Annotated[str, TEXT]


@dataclass
class SerialNumber(XmlModel, regclass=AnIMLDocBase):
    """
    Unique serial number of device

    Text:
        value (str): Serial number value
    """

    # Text
    value: Annotated[str, TEXT]


@dataclass
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
    identifier: Annotated[Optional[DeviceIdentifier], CHILD]
    manufacturer: Annotated[Optional[Manufacturer], CHILD]
    name: Annotated[Name, CHILD]
    firmware: Annotated[Optional[FirmwareVersion], CHILD]
    serialNumber: Annotated[Optional[SerialNumber], CHILD]
