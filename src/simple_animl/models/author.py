from enum import Enum
from typing import Optional

from ..core import Field, XmlModel
from ..utils.regex import NC_NAME
from .base import AnIMLDocBase
from .common import Name


class UserType(str, Enum):
    Human = "human"
    Device = "device"
    Software = "software"


class Author(XmlModel, regclass=AnIMLDocBase):
    """
    Information about a person, a device or a piece of software authoring AnIML files.

    Attributes:
        userType (UserType): Type of user (human, device, software)

    Children:
        name (Name): Common name of the author
    """

    # Attributes
    userType: UserType = Field.Attribute()

    # Children
    name: Name = Field.Child()
