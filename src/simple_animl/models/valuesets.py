from typing import List, Optional, Union

from ..core import Field, XmlModel
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


class AutoIncrementedValueSet(XmlModel, regclass=AnIMLDocBase):
    """Multiple values given in form of a start value and an increment.

    Attributes:
        endIndex (int): Zero-based index of the last entry in this Value Set. The specification is inclusive.
        startIndex (int): Zero-based index of the first entry in this Value Set. The specification is inclusive.

    Children:
        startValue (Union[DoubleType, FloatType, IntType, LongType]): Lower boundary of an interval or ValueSet.
        increment (Union[DoubleType, FloatType, IntType, LongType]): Increment value
    """

    endIndex: Optional[int] = Field.Attribute(**SERIALIZE_INT)
    startIndex: Optional[int] = Field.Attribute(**SERIALIZE_INT)

    startValue: Union[DoubleType, FloatType, IntType, LongType] = Field.Child()
    increment: Union[DoubleType, FloatType, IntType, LongType] = Field.Child()


class EncodedValueSet(XmlModel, regclass=AnIMLDocBase):
    """Multiple numeric values encoded as a base64 binary string. Uses little-endian byte order.

    Attributes:
        endIndex (int): Zero-based index of the last entry in this Value Set. The specification is inclusive.
        startIndex (int): Zero-based index of the first entry in this Value Set. The specification is inclusive.

    Text:
        value (bytes): Base64 encoded binary data

    """

    endIndex: Optional[int] = Field.Attribute(**SERIALIZE_INT)
    startIndex: Optional[int] = Field.Attribute(**SERIALIZE_INT)

    value: Optional[bytes] = Field.Text(**SERIALIZE_BINARY)


class IndividualValueSet(XmlModel, regclass=AnIMLDocBase):
    """Multiple Values explicitly specified.

    Attributes:
        endIndex (int): Zero-based index of the last entry in this Value Set. The specification is inclusive.
        startIndex (int): Zero-based index of the first entry in this Value Set. The specification is inclusive.

    Children:
        values (list[Union[BooleanType, DoubleType, DateTimeType, EmbeddedXmlType, FloatType, IntType, LongType, \
            PNGType, StringType, SVGType]]): A set of Value elements.
    """

    endIndex: Optional[int] = Field.Attribute(**SERIALIZE_INT)
    startIndex: Optional[int] = Field.Attribute(**SERIALIZE_INT)
    values: Optional[
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
        ]
    ] = Field.Child()
