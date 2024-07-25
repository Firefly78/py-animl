from dataclasses import dataclass
from enum import Enum
from typing import Annotated

from ..core import ATTRIB, CHILD, XmlModel
from .base import AnIMLDocBase
from .common import Name


class UserType(str, Enum):
    Human = "human"
    Device = "device"
    Software = "software"


AnIMLDocBase.register(UserType.__name__, UserType)


@dataclass
class Author(XmlModel, regclass=AnIMLDocBase):
    """
    Information about a person, a device or a piece of software authoring AnIML files.

    ```xml
    <Author userType="human">
        <Name>...</Name>
    </Author>
    ```

    Attributes:
        userType (UserType): Type of user (human, device, software)
        name (Name): Common name of the author
    """

    # Attributes
    userType: Annotated[UserType, ATTRIB]

    # Children
    name: Annotated[Name, CHILD]
