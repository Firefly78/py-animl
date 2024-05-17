from __future__ import annotations

from typing import Optional

from ..core import Field, XmlModel
from ..utils.regex import NC_NAME
from .base import AnIMLDocBase
from .category import Category
from .tags import TagSet

# Need have it serialized as true/false, not True/False
SERIALIZE_BOOL = {
    "on_serialize": lambda x: "true" if x else "false",
    "on_deserialize": lambda x: x == "true",
}


class Sample(XmlModel, regclass=AnIMLDocBase):
    """
    Individual Sample, referenced from other parts of this AnIML document.

    Attributes:
        name (str): Plain-text name of this item.
        sampleID (str): Token with up to 1024 characters

        barcode (str): Value of barcode label that is attached to sample container.
        comment (str): Unstructured text comment to further describe the Sample.
        containerID (str): Sample ID of container in which this sample is located.
        containerType (str): Whether this sample is also a container for other samples. \
                Set to "simple" if not.
        derived (bool): Indicates whether this is a derived Sample. A derived Sample \
                is a Sample that has been created by applying a Technique. \
                (Sub-Sampling, Processing, ...).
        id (str): Anchor point for digital signature. This identifier is referred \
                to from the "Reference" element in a Signature. Unique per document.
        locationInContainer (str): Coordinates of this sample within the enclosing \
                container. In case of microplates or trays, the row is identified \
                by letters and the column is identified by numbers (1-based) while \
                in landscape orientation. Examples: A10 = 1st row, 10th column, \
                Z1 = 26th row, 1st column, AB2 = 28th row, 2nd column.
        sourceDataLocation (str): Points to the original data source. May be a \
                file name, uri, database ID, etc.

    Children:
        tag_set (TagSet): Set of Tag elements.
        category (Category): Defines a category of Parameters and SeriesSets. Used \
                to model hierarchies.

    """

    # Mandatory fields
    name: str = Field.Attribute()
    sampleID: str = Field.Attribute()

    # Optional fields
    barcode: Optional[str] = Field.Attribute()
    comment: Optional[str] = Field.Attribute()
    containerID: Optional[str] = Field.Attribute()
    containerType: Optional[str] = Field.Attribute()
    derived: Optional[bool] = Field.Attribute(**SERIALIZE_BOOL)
    id: Optional[str] = Field.Attribute(regex=NC_NAME)
    locationInContainer: Optional[str] = Field.Attribute()
    sourceDataLocation: Optional[str] = Field.Attribute()

    # Children
    tag_set: Optional[TagSet] = Field.Child()
    category: Optional[Category] = Field.Child()


class SampleSet(XmlModel, regclass=AnIMLDocBase):
    """
    Container for Samples used in this AnIML document.

    Attributes:
        id (str): Anchor point for digital signature. This identifier is referred \
              to from the "Reference" element in a Signature. Unique per document.

    Children:
        samples (list[Sample]): Individual Samples
    """

    # Optional fields
    id: Optional[str] = Field.Attribute(regex=NC_NAME)

    # Children
    samples: list[Sample] = Field.Child(default_factory=list)

    def add(self, sample: Sample) -> None:
        if self.samples is None:
            self.samples = list()
        self.samples.append(sample)
