from __future__ import annotations

from enum import Enum
from typing import Optional, Union

from ..core import Field, XmlModel
from ..utils.regex import NC_NAME
from .data_type import (
    BooleanType,
    DateTimeType,
    DoubleType,
    EmbeddedXmlType,
    FloatType,
    IntType,
    LongType,
    PNGType,
    StringType,
    SVGType,
)
from .unit import Unit


class ParameterTypes(str, Enum):
    Int32 = "Int32"
    Int64 = "Int64"
    Float32 = "Float32"
    Float64 = "Float64"
    String = "String"
    Boolean = "Boolean"
    DateTime = "DateTime"
    EmbeddedXML = "EmbeddedXML"
    PNG = "PNG"
    SVG = "SVG"


class Parameter(XmlModel):
    """
    Name/Value Pair.
    
    Attributes:
        name (str): Plain-text name of this item.
        parameterType (str): Data type of this parameter
        id (str): Anchor point for digital signature. This identifier is referred \
                to from the "Reference" element in a Signature. Unique per document.
        
    Children:
        value: (??): Individual value
        unit (Unit): Definition of a Scientific Unit.

    """

    name: str = Field.Attribute()
    parameterType: ParameterTypes = Field.Attribute()
    id: Optional[str] = Field.Attribute(regex=NC_NAME)

    value: Union[
        BooleanType,
        DoubleType,
        DateTimeType,
        EmbeddedXmlType,
        FloatType,
        IntType,
        LongType,
        PNGType,
        StringType,
        SVGType,
    ] = Field.Child()
    unit: Optional[Unit] = Field.Child()
