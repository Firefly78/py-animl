from dataclasses import dataclass
from typing import Annotated, Optional

from ..core import ATTRIB, CHILD, XmlModel
from ..utils.regex import NC_NAME
from .author import Author
from .base import AnIMLDocBase
from .category import Category
from .device import Device
from .software import Software


@dataclass
class Method(XmlModel, regclass=AnIMLDocBase):
    """
    Describes how this Experiment was performed.

    ```xml
    <Method id="..." name="...">
        <Author .../>
        <Device .../>
        <Software .../>
        <Category .../>
    </Method>
    ```

    Attributes:
        name (str | None): Optional method name, as defined in the instrument software.
        id (str | None): Anchor point for digital signature. This identifier is referred \
            to from the "Reference" element in a Signature. Unique per document.
        author (Author | None): Information about the person, device or software that authored this Method.
        device (Device | None): Device used to perform experiment.
        software (Software | None): Software used to author this.
        category (Category | None): Defines a category of Parameters and SeriesSets. Used to model hierarchies.
    """

    # Attributes
    name: Annotated[Optional[str], ATTRIB]
    id: Annotated[Optional[str], ATTRIB(regex=NC_NAME)]

    # Children
    author: Annotated[Optional[Author], CHILD]
    device: Annotated[Optional[Device], CHILD]
    software: Annotated[Optional[Software], CHILD]
    category: Annotated[Optional[Category], CHILD]
