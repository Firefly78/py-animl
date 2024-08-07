from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Annotated, Optional, Union

from ..core import ATTRIB, CHILD, XmlModel
from ..utils.regex import NC_NAME
from .base import AnIMLDocBase
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


class ParameterType(str, Enum):
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


AnIMLDocBase.register(ParameterType.__name__, ParameterType)


@dataclass
class Parameter(XmlModel, regclass=AnIMLDocBase):
    """
    Name/Value Pair.

    ```xml
    <Parameter name="..." parameterType="..." id="...">
        <F>...</F> 
        <Unit .../>
    </Parameter>
    ```

    Attributes:
        name (str): Plain-text name of this item.
        parameterType (str): Data type of this parameter
        id (str | None): Anchor point for digital signature. This identifier is referred \
                to from the "Reference" element in a Signature. Unique per document.
        value (BooleanType | DoubleType | DateTimeType | ...): Individual value
        unit (Unit | None): Definition of a Scientific Unit.

    """

    name: Annotated[str, ATTRIB]
    parameterType: Annotated[ParameterType, ATTRIB]
    id: Annotated[Optional[str], ATTRIB(regex=NC_NAME)] = None

    value: Annotated[
        Optional[
            Union[
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
            ]
        ],
        CHILD,
    ] = None
    unit: Annotated[Optional[Unit], CHILD] = None
