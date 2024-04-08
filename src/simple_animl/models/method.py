from typing import Optional

from ..core import Field, XmlModel
from ..utils.regex import NC_NAME
from .author import Author
from .base import AnIMLDocBase
from .category import Category
from .device import Device
from .software import Software


class Method(XmlModel, regclass=AnIMLDocBase):
    """
    Describes how this Experiment was performed.

    Attributes:
        name (str): Optional method name, as defined in the instrument software.
        id (str): Anchor point for digital signature. This identifier is referred \
            to from the "Reference" element in a Signature. Unique per document.

    Children:
        author (Author): Information about the person, device or software that authored this Method.
        device (Device): Device used to perform experiment.
        software (Software): Software used to author this.
        category (Category): Defines a category of Parameters and SeriesSets. Used to model hierarchies.
    """

    # Attributes
    name: str = Field.Attribute()
    id: Optional[str] = Field.Attribute(regex=NC_NAME)

    # Children
    author: Optional[Author] = Field.Child()
    device: Optional[Device] = Field.Child()
    software: Optional[Software] = Field.Child()
    category: Optional[Category] = Field.Child()
