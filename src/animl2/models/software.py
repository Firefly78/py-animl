from dataclasses import dataclass
from typing import Annotated, Optional

from ..core import CHILD, TEXT, XmlModel
from .base import AnIMLDocBase
from .common import Manufacturer, Name


@dataclass
class OperatingSystem(XmlModel, regclass=AnIMLDocBase):
    """
    Operating system the software was running on.

    Text:
        value (str): Operating system value
    """

    # Text
    value: Annotated[str, TEXT]


@dataclass
class Version(XmlModel, regclass=AnIMLDocBase):
    """
    Version identifier of software release.

    Text:
        value (str): Version value
    """

    # Text
    value: Annotated[str, TEXT]


@dataclass
class Software(XmlModel, regclass=AnIMLDocBase):
    """
    Software used to author this.

    Children:
        name (Name): Common name.
        manufacturer (Manufacturer): Company name.
        version (optional(Version)): Version identifier of software release.
        operating_system (optional(OperatingSystem)): Operating system the software was running on.
    """

    # Children
    name: Annotated[Name, CHILD]
    manufacturer: Annotated[Manufacturer, CHILD]
    version: Annotated[Optional[Version], CHILD]
    operating_system: Annotated[Optional[OperatingSystem], CHILD]
