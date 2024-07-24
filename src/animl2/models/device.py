from dataclasses import dataclass
from typing import Annotated, Optional

from ..core import ATTRIB, CHILD, TEXT, XmlModel
from .base import AnIMLDocBase
from .common import Manufacturer, Name


@dataclass
class DeviceIdentifier(XmlModel, regclass=AnIMLDocBase):
    """
    Unique name or identifier of the device.

    ```xml
    <DeviceIdentifier>...</DeviceIdentifier>

    ```

    Attributes:
        value (str): Identifier value
    """

    # Text
    value: Annotated[str, TEXT]


@dataclass
class FirmwareVersion(XmlModel, regclass=AnIMLDocBase):
    """
    Version identifier of firmware release.

    ```xml
    <FirmwareVersion>...</FirmwareVersion>

    ```

    Attributes:
        value (str): Firmware version value
    """

    # Text
    value: Annotated[str, TEXT]


@dataclass
class SerialNumber(XmlModel, regclass=AnIMLDocBase):
    """
    Unique serial number of device

    ```xml
    <SerialNumber>...</SerialNumber>

    ```

    Attributes:
        value (str): Serial number value
    """

    # Text
    value: Annotated[str, TEXT]


@dataclass
class Device(XmlModel, regclass=AnIMLDocBase):
    """
    Device used to perform experiment.

    ```xml
    <Device>
        <DeviceIdentifier>...</DeviceIdentifier>
        <Manufacturer>...</Manufacturer>
        <Name>...</Name>
        <FirmwareVersion>...</FirmwareVersion>
        <SerialNumber>...</SerialNumber>
    </Device>
    ```

    Attributes:
        identifier (DeviceIdentifier | None): Unique name or identifier of the device.
        manufacturer (Manufacturer | None): Company name.
        name (Name): Common name.
        firmware (Firmware | None): Version identifier of firmware release.
        serialNumber (SerialNumber | None): Unique serial number of device

    """

    # Children
    identifier: Annotated[Optional[DeviceIdentifier], CHILD]
    manufacturer: Annotated[Optional[Manufacturer], CHILD]
    name: Annotated[Name, CHILD]
    firmware: Annotated[Optional[FirmwareVersion], CHILD]
    serialNumber: Annotated[Optional[SerialNumber], CHILD]
