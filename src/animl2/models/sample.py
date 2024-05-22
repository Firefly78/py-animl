from __future__ import annotations

from dataclasses import dataclass, field
from typing import Annotated, Optional

from ..core import ATTRIB, CHILD, XmlModel
from ..utils.regex import NC_NAME
from .base import AnIMLDocBase
from .category import Category
from .tags import Tag, TagSet

# Need have it serialized as true/false, not True/False
SERIALIZE_BOOL = {
    "on_serialize": lambda x: "true" if x else "false",
    "on_deserialize": lambda x: x == "true",
}


@dataclass
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
    name: Annotated[str, ATTRIB]
    sampleID: Annotated[str, ATTRIB]

    # Optional fields
    barcode: Annotated[Optional[str], ATTRIB] = None
    comment: Annotated[Optional[str], ATTRIB] = None
    containerID: Annotated[Optional[str], ATTRIB] = None
    containerType: Annotated[Optional[str], ATTRIB] = None
    derived: Annotated[Optional[bool], ATTRIB(**SERIALIZE_BOOL)] = None
    id: Annotated[Optional[str], ATTRIB(regex=NC_NAME)] = None
    locationInContainer: Annotated[Optional[str], ATTRIB] = None
    sourceDataLocation: Annotated[Optional[str], ATTRIB] = None

    # Children
    tag_set: Annotated[Optional[TagSet], CHILD] = None
    category: Annotated[Optional[Category], CHILD] = None

    def append(self, item: Tag):
        if self.tag_set is None:
            self.tag_set = TagSet()
        return self.tag_set.append(item)


@dataclass
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
    id: Annotated[Optional[str], ATTRIB(regex=NC_NAME)] = None

    # Children
    samples: Annotated[list[Sample], CHILD] = field(default_factory=list)

    def append(self, sample: Sample):
        if self.samples is None:
            self.samples = list()
        self.samples.append(sample)
        return sample
