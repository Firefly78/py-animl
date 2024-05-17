from enum import Enum

from ..core import Field, XmlModel
from .base import AnIMLDocBase
from .common import Name


class UserType(str, Enum):
    Human = "human"
    Device = "device"
    Software = "software"


AnIMLDocBase.register(UserType.__name__, UserType)


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
