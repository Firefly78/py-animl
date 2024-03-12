from __future__ import annotations

from enum import Enum
from typing import Optional

from ..core import Field, XmlModel


class Unit(XmlModel):
    """
    Definition of a Scientific Unit.

    Attributes:
        label (str): Defines the visual representation of a particular Unit.
        quantity (str): Quantity the unit can be applied to

    Children:
        siunits (list[SIUnit]): Combination of SI Units used to represent Scientific Unit
    """

    label: str = Field.Attribute()
    quantity: Optional[str] = Field.Attribute()

    siunits: Optional[list[SIUnit]] = Field.Child()


class UnitText(str, Enum):
    Unitless = "1"
    Meter = "m"
    Kg = "kg"
    Second = "s"
    Ampere = "A"
    Kelving = "K"
    Molare = "mol"
    Candela = "cd"


XmlModel.register_type(UnitText)


class SIUnit(XmlModel):
    """
    Combination of SI Units used to represent Scientific Unit.

    Attributes:
        exponent (Optional[str]): Exponent of the SI Unit
        factor (Optional[str]): Factor of the SI Unit
        offset (Optional[str]): Offset of the SI Unit

    Children:
        unit (str): Unit of the SI Unit, (default: UnitText.Unitless)
    """

    exponent: Optional[str] = Field.Attribute()
    factor: Optional[str] = Field.Attribute()
    offset: Optional[str] = Field.Attribute()

    unit: UnitText = Field.Text(default=UnitText.Unitless)
