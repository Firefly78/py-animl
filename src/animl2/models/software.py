from typing import Optional

from ..core import Field, XmlModel
from .base import AnIMLDocBase
from .common import Manufacturer, Name


class OperatingSystem(XmlModel, regclass=AnIMLDocBase):
    """
    Operating system the software was running on.

    Text:
        value (str): Operating system value
    """

    # Text
    value: str = Field.Text()


class Version(XmlModel, regclass=AnIMLDocBase):
    """
    Version identifier of software release.

    Text:
        value (str): Version value
    """

    # Text
    value: str = Field.Text()


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
    name: Name = Field.Child()
    manufacturer: Manufacturer = Field.Child()
    version: Optional[Version] = Field.Child()
    operating_system: Optional[OperatingSystem] = Field.Child()
