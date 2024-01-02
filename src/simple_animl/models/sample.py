from __future__ import annotations

from typing import Optional

from ..core import Field, XmlModel
from .category import Category
from .tags import TagSet


class Sample(XmlModel):
    """
    Individual Sample, referenced from other parts of this AnIML document.

    Args:
        name (str): Plain-text name of this item.
        sampleID (str): Token with up to 1024 characters
    """

    # Mandatory fields
    name: str = Field.Attribute()
    sampleID: str = Field.Attribute()

    # Optional fields
    # TBD: Lots of fields to be added here

    # Children
    tag_set: Optional[TagSet] = Field.Child()
    category: Optional[Category] = Field.Child()


class SampleSet(XmlModel):
    """
    Container for Samples used in this AnIML document.
    
    Args:
        id (str): Anchor point for digital signature. This identifier is referred \
              to from the "Reference" element in a Signature. Unique per document.
    """

    # Optional fields
    id: Optional[str] = Field.Attribute()

    # Children
    samples: list[Sample] = Field.Child(default_factory=list)

    def add(self, sample: Sample) -> None:
        if self.samples is None:
            self.samples = list()
        self.samples.append(sample)
