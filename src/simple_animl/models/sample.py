from __future__ import annotations

from typing import Optional

from pydantic import Field

from ..utils.regex import NC_NAME
from .core import XmlModel


def myfunc(a, *, b):
    """_summary_

    Args:
        a (_type_): _description_
        b (_type_): _description_

    Returns:
        _type_: _description_
    """
    return a + b


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
    # TBD: Lots of children to be added here


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
