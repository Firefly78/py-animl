from __future__ import annotations

from io import StringIO
from typing import IO, Optional, Union
from xml.etree.ElementTree import ElementTree

from ..core import Field, XmlModel
from .sample import SampleSet

VERSION: str = "0.90"
XMLNS: str = "urn:org:astm:animl:schema:core:draft:0.90"
XMLNS_XSI: str = "http://www.w3.org/2001/XMLSchema-instance"
XSI_SCHEMALOCATION: str = "urn:org:astm:animl:schema:core:draft:0.90 http://schemas.animl.org/current/animl-core.xsd"


class AnIMLDoc(XmlModel):
    """
    Root Element for AnIML documents.

    Attributes:
        version (str): Version of AnIML
        xmlns (str): XML namespace
        xmlns_xsi (str): XML namespace for schema instance
        xsi_schemalocation (str): Schema location

    Children:
        sample_set (SampleSet): Collection of Samples
        TODO: Add more children

    """

    tag = "AnIML"  # Override name to use during serialization

    # Manadatory attributes
    version: Optional[str] = Field.Attribute(default=VERSION)
    xmlns: Optional[str] = Field.Attribute(default=XMLNS)
    xmlns_xsi: Optional[str] = Field.Attribute(default=XMLNS_XSI, alias="xmlns:xsi")
    xsi_schemalocation: Optional[str] = Field.Attribute(
        default=XSI_SCHEMALOCATION, alias="xsi:schemaLocation"
    )

    sample_set: Optional[SampleSet] = Field.Child()

    @classmethod
    def loads(cls, xml: Union[IO, str]) -> AnIMLDoc:
        if isinstance(xml, str):
            xml = StringIO(xml)
        elif isinstance(xml, IO):
            pass  # Nothing
        else:
            raise TypeError(f"Expected str or IO, got {type(xml)}")
        et = ElementTree()
        et.parse(source=xml)
        return cls.load_xml(et.getroot())
