from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Annotated, Optional, overload

from ..core import ATTRIB, CHILD, TEXT, XmlModel
from .base import AnIMLDocBase


@dataclass
class Unit(XmlModel, regclass=AnIMLDocBase):
    """
    Definition of a Scientific Unit.

    ```xml
    <Unit label="..." quantity="...">
        <SIUnit unit="..."/>
    </Unit>
    ```

    Attributes:
        label (str): Defines the visual representation of a particular Unit.
        quantity (str | None): Quantity the unit can be applied to

        siunits (list[SIUnit] | None): Combination of SI Units used to represent Scientific Unit
    """

    label: Annotated[str, ATTRIB]
    quantity: Annotated[Optional[str], ATTRIB] = None

    siunits: Annotated[Optional[list[SIUnit]], CHILD] = None

    @overload
    def append(self, item: SIUnit) -> SIUnit:
        """Add a SIUnit to this Unit"""

    def append(self, item):
        if self.siunits is None:
            self.siunits = list()
        self.siunits.append(item)
        return item


class UnitText(str, Enum):
    Unitless = "1"
    Meter = "m"
    Kg = "kg"
    Second = "s"
    Ampere = "A"
    Kelving = "K"
    Molare = "mol"
    Candela = "cd"


AnIMLDocBase.register(UnitText.__name__, UnitText)


@dataclass
class SIUnit(XmlModel, regclass=AnIMLDocBase):
    """
    Combination of SI Units used to represent Scientific Unit.

    ```xml
    <SIUnit exponent="..." factor="..." offset="...">cd</SIUnit>

    ```

    Attributes:
        exponent (str | None): Exponent of the SI Unit
        factor (str | None): Factor of the SI Unit
        offset (str | None): Offset of the SI Unit

        unit (UnitText): Unit of the SI Unit, (default: UnitText.Unitless)
    """

    exponent: Annotated[Optional[str], ATTRIB] = None
    factor: Annotated[Optional[str], ATTRIB] = None
    offset: Annotated[Optional[str], ATTRIB] = None

    unit: Annotated[UnitText, TEXT] = field(default=UnitText.Unitless)
