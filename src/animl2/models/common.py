from dataclasses import dataclass
from typing import Annotated

from ..core import TEXT, XmlModel
from .base import AnIMLDocBase


@dataclass
class Name(XmlModel, regclass=AnIMLDocBase):
    """
    Common name.

    ```xml
    <Name>...</Name>

    ```

    Attributes:
        value (str): Name value

    """

    # Text
    value: Annotated[str, TEXT]


@dataclass
class Manufacturer(XmlModel, regclass=AnIMLDocBase):
    """
    Company name.

    ```xml
    <Manufacturer>...</Manufacturer>

    ```

    Attributes:
        value (str): Manufacturer value
    """

    # Text
    value: Annotated[str, TEXT]
