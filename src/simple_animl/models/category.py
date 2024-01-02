from __future__ import annotations

from typing import Optional

from ..core import Field, XmlModel


class Category(XmlModel):
    """
    Defines a category of Parameters and SeriesSets. Used to model hierarchies.

    Args:
        name (str): Plain-text name of this item.
        id (str): Anchor point for digital signature. This identifier is referred \
              to from the "Reference" element in a Signature. Unique per document.

    """

    name: str = Field.Attribute()
    id: Optional[str] = Field.Attribute()

    # parameters: list[Parameter] = Field.Child()
    # series_sets: list[SeriesSet] = Field.Child()
    sub_categories: list[Category] = Field.Child()
