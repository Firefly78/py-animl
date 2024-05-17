from typing import Optional

from ..core import Field, XmlModel
from ..utils.regex import NC_NAME
from .base import AnIMLDocBase


class Extension(XmlModel, regclass=AnIMLDocBase):
    """
    Reference to an Extension to amend the active Technique Definition.

    Attributes:
        name (str): Name of Extension to be used. Must match Name given in \
            Extension Definition file.
        uri (str): URI where Extension file can be fetched.
        sha256 (str): SHA256 checksum of the referenced Extension. Hex encoded, \
            lower cased. Similar to the output of the sha256 unix command.
    """

    # Attributes
    name: str = Field.Attribute()
    uri: str = Field.Attribute()
    sha256: Optional[str] = Field.Attribute()


class Technique(XmlModel, regclass=AnIMLDocBase):
    """
    Reference to Technique Definition used in this Experiment.

    Attributes:
        name (str): Plain-text name of this item.
        uri (str): URI where Technique Definition file can be fetched.
        id (str): Anchor point for digital signature. This identifier is \
            referred to from the "Reference" element in a Signature. Unique per document.
        sha256 (str): SHA256 checksum of the referenced Technique Definition. \
            Hex encoded, lower cased. Similar to the output of the sha256 unix command.

    Children:
        extensions (Extension): Set of extension elements.
    """

    # Attributes
    name: str = Field.Attribute()
    uri: str = Field.Attribute()
    id: Optional[str] = Field.Attribute(regex=NC_NAME)
    sha256: Optional[str] = Field.Attribute()

    # Children
    extensions: Optional[list[Extension]] = Field.Child()
