from __future__ import annotations

from typing import Optional, Union

from ..core import Field, XmlModel
from .base import AnIMLDocBase
from .parameter import Parameter
from .series import SeriesSet


class Category(XmlModel, regclass=AnIMLDocBase):
    """
    Defines a category of Parameters and SeriesSets. Used to model hierarchies.

    Attributes:
        name (str): Plain-text name of this item.
        id (str): Anchor point for digital signature. This identifier is referred \
              to from the "Reference" element in a Signature. Unique per document.

    Children:
        parameters (list[Parameter]): List of Parameters that are part of this Category.
        series_sets (list[SeriesSet]): List of SeriesSets that are part of this Category.
        sub_categories (list[Category]): List of sub-categories that are part of this Category.

    """

    name: str = Field.Attribute()
    id: Optional[str] = Field.Attribute()

    parameters: Optional[list[Parameter]] = Field.Child()
    series_sets: Optional[list[SeriesSet]] = Field.Child()
    sub_categories: Optional[list[Category]] = Field.Child()

    def append(self, item: Union[Parameter, SeriesSet, Category]):
        """Add and return a sub-item to this category"""
        if isinstance(item, Parameter):
            if self.parameters is None:
                self.parameters = list()
            self.parameters.append(item)
        elif isinstance(item, SeriesSet):
            if self.series_sets is None:
                self.series_sets = list()
            self.series_sets.append(item)
        elif isinstance(item, Category):
            if self.sub_categories is None:
                self.sub_categories = list()
            self.sub_categories.append(item)
        else:
            raise ValueError(f"Unknown item type: {type(item)}")

        return item
