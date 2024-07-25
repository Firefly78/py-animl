from dataclasses import dataclass
from typing import Annotated, Optional

from ..core import CHILD, TEXT, XmlModel
from .base import AnIMLDocBase
from .common import Manufacturer, Name


@dataclass
class OperatingSystem(XmlModel, regclass=AnIMLDocBase):
    """
    Operating system the software was running on.

    ```xml
    <OperatingSystem>...</OperatingSystem>

    ```

    Attributes:
        value (str): Operating system value
    """

    # Text
    value: Annotated[str, TEXT]


@dataclass
class Version(XmlModel, regclass=AnIMLDocBase):
    """
    Version identifier of software release.

    ```xml
    <Version>...</Version>

    ```

    Attributes:
        value (str): Version value
    """

    # Text
    value: Annotated[str, TEXT]


@dataclass
class Software(XmlModel, regclass=AnIMLDocBase):
    """
    Software used to author this.

    ```xml
    <Software>
        <Name>...</Name>
        <Manufacturer>...</Manufacturer>
        <Version>...</Version>
        <OperatingSystem>...</OperatingSystem>
    </Software>
    ```

    Attributes:
        name (Name): Common name.
        manufacturer (Manufacturer): Company name.
        version (Version | None): Version identifier of software release.
        operating_system (OperatingSystem | None): Operating system the software was running on.
    """

    # Children
    name: Annotated[Name, CHILD]
    manufacturer: Annotated[Manufacturer, CHILD]
    version: Annotated[Optional[Version], CHILD]
    operating_system: Annotated[Optional[OperatingSystem], CHILD]
