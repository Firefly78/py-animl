from __future__ import annotations

from dataclasses import dataclass, field
from typing import Annotated, Optional, TypeVar, Union, overload

from ..core import ATTRIB, CHILD, XmlModel
from .base import AnIMLDocBase
from .parameter import Parameter
from .series import SeriesSet


@dataclass
class Category(XmlModel, regclass=AnIMLDocBase):
    """
    Defines a category of Parameters and SeriesSets. Used to model hierarchies.

    ```xml
    <Category name="..." id="...">
        <Parameter .../>
        <SeriesSet .../>
        <Category .../>
    </Category>
    ```

    Attributes:
        name (str): Plain-text name of this item.
        id (str | None): Anchor point for digital signature. This identifier is referred \
              to from the "Reference" element in a Signature. Unique per document.
        parameters (list[Parameter] | None): List of Parameters that are part of this Category.
        series_sets (list[SeriesSet] | None): List of SeriesSets that are part of this Category.
        sub_categories (list[Category] | None): List of sub-categories that are part of this Category.

    """

    name: Annotated[str, ATTRIB]
    id: Annotated[Optional[str], ATTRIB] = None

    parameters: Annotated[Optional[list[Parameter]], CHILD] = field(
        default_factory=list
    )
    series_sets: Annotated[Optional[list[SeriesSet]], CHILD] = field(
        default_factory=list
    )
    sub_categories: Annotated[Optional[list[Category]], CHILD] = field(
        default_factory=list
    )

    @overload
    def append(self, item: Parameter) -> Parameter:
        """Adda Parameter to this category"""

    @overload
    def append(self, item: SeriesSet) -> SeriesSet:
        """Add a SeriesSet to this category"""

    @overload
    def append(self, item: Category) -> Category:
        """Add a sub-category to this category"""

    def append(self, item):
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
            raise TypeError(
                f"Expected Parameter, SeriesSet, or Category, got {type(item)}"
            )

        return item
