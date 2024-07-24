from dataclasses import dataclass
from typing import Annotated, List, Optional, Union

from ..core import ATTRIB, CHILD, TEXT, XmlModel
from .base import AnIMLDocBase
from .data_type import (
    SERIALIZE_BINARY,
    SERIALIZE_INT,
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


@dataclass
class AutoIncrementedValueSet(XmlModel, regclass=AnIMLDocBase):
    """Multiple values given in form of a start value and an increment.

    Attributes:
        endIndex (int): Zero-based index of the last entry in this Value Set. The specification is inclusive.
        startIndex (int): Zero-based index of the first entry in this Value Set. The specification is inclusive.

    Children:
        startValue (Union[DoubleType, FloatType, IntType, LongType]): Lower boundary of an interval or ValueSet.
        increment (Union[DoubleType, FloatType, IntType, LongType]): Increment value
    """

    startValue: Annotated[Union[DoubleType, FloatType, IntType, LongType], CHILD]
    increment: Annotated[Union[DoubleType, FloatType, IntType, LongType], CHILD]

    endIndex: Annotated[Optional[int], ATTRIB(**SERIALIZE_INT)] = None
    startIndex: Annotated[Optional[int], ATTRIB(**SERIALIZE_INT)] = None


@dataclass
class EncodedValueSet(XmlModel, regclass=AnIMLDocBase):
    """Multiple numeric values encoded as a base64 binary string. Uses little-endian byte order.

    Attributes:
        endIndex (int): Zero-based index of the last entry in this Value Set. The specification is inclusive.
        startIndex (int): Zero-based index of the first entry in this Value Set. The specification is inclusive.

    Text:
        value (bytes): Base64 encoded binary data

    """

    value: Annotated[Optional[bytes], TEXT(**SERIALIZE_BINARY)]

    endIndex: Annotated[Optional[int], ATTRIB(**SERIALIZE_INT)] = None
    startIndex: Annotated[Optional[int], ATTRIB(**SERIALIZE_INT)] = None


@dataclass
class IndividualValueSet(XmlModel, regclass=AnIMLDocBase):
    """Multiple Values explicitly specified.

    Attributes:
        endIndex (int): Zero-based index of the last entry in this Value Set. The specification is inclusive.
        startIndex (int): Zero-based index of the first entry in this Value Set. The specification is inclusive.

    Children:
        values (list[Union[BooleanType, DoubleType, DateTimeType, EmbeddedXmlType, FloatType, IntType, LongType, \
            PNGType, StringType, SVGType]]): A set of Value elements.
    """

    values: Annotated[
        List[
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
    ]

    endIndex: Annotated[Optional[int], ATTRIB(**SERIALIZE_INT)] = None
    startIndex: Annotated[Optional[int], ATTRIB(**SERIALIZE_INT)] = None
