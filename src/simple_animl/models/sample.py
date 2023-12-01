from __future__ import annotations

from typing import Optional

from pydantic import Field

from ..utils.regex import NC_NAME
from .core import XmlModel
from .tags import TagSet


class Sample(XmlModel):
    """
    Individual Sample, referenced from other parts of this AnIML document.

    Args:
        name (str): Plain-text name of this item.
        sampleID (str): Token with up to 1024 characters
    """

    # Mandatory fields
    name: str = Field(..., description="Plain-text name of this item.")
    sampleID: str = Field(..., description="Token with up to 1024 characters")

    # Optional fields
    # TBD: Lots of fields to be added here

    # Children

    tag_set: Optional[TagSet] = None

    @classmethod
    def load_xml(cls, node) -> Sample:
        if node is None:
            return None
        return cls(
            name=node.attrib.get("name"),
            sampleID=node.attrib.get("sampleID"),
            tag_set=TagSet.load_xml(node.find("TagSet")),
        )


class SampleSet(XmlModel):
    """
    Container for Samples used in this AnIML document.
    
    Args:
        id (str): Anchor point for digital signature. This identifier is referred \
              to from the "Reference" element in a Signature. Unique per document.
    """

    # Optional fields
    id: Optional[str] = Field(
        default=None,
        pattern=NC_NAME,
        description='Anchor point for digital signature. This identifier is referred \
              to from the "Reference" element in a Signature. Unique per document.',
    )

    # Children
    samples: list[Sample] = Field(default_factory=list)

    @classmethod
    def load_xml(cls, node) -> SampleSet:
        if node is None:
            return None
        return cls(
            id=node.attrib.get("id"),
            samples=[Sample.load_xml(n) for n in node.findall("Sample")],
        )
