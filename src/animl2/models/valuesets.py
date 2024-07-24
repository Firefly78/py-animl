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
from .infrastructure import Increment, StartValue


@dataclass
class AutoIncrementedValueSet(XmlModel, regclass=AnIMLDocBase):
    """Multiple values given in form of a start value and an increment.

    ```xml
    <AutoIncrementedValueSet startIndex="..." endIndex="...">
        <StartValue>...</StartValue>
        <Increment>...</Increment>
    </AutoIncrementedValueSet>
    ```

    Attributes:
        endIndex (int): Zero-based index of the last entry in this Value Set. The specification is inclusive.
        startIndex (int): Zero-based index of the first entry in this Value Set. The specification is inclusive.

        startValue (StartValue | None): Lower boundary of an interval or ValueSet.
        increment (Increment | None): Increment value
    """

    startValue: Annotated[StartValue, CHILD]
    increment: Annotated[Increment, CHILD]

    endIndex: Annotated[Optional[int], ATTRIB(**SERIALIZE_INT)] = None
    startIndex: Annotated[Optional[int], ATTRIB(**SERIALIZE_INT)] = None


@dataclass
class EncodedValueSet(XmlModel, regclass=AnIMLDocBase):
    """Multiple numeric values encoded as a base64 binary string. Uses little-endian byte order.

    ```xml
    <EncodedValueSet startIndex="..." endIndex="...">002A</EncodedValueSet>

    ```

    Attributes:
        endIndex (int | None): Zero-based index of the last entry in this Value Set. The specification is inclusive.
        startIndex (int | None): Zero-based index of the first entry in this Value Set. The specification is inclusive.

        value (bytes | None): Base64 encoded binary data
    """

    value: Annotated[Optional[bytes], TEXT(**SERIALIZE_BINARY)]

    endIndex: Annotated[Optional[int], ATTRIB(**SERIALIZE_INT)] = None
    startIndex: Annotated[Optional[int], ATTRIB(**SERIALIZE_INT)] = None


@dataclass
class IndividualValueSet(XmlModel, regclass=AnIMLDocBase):
    """Multiple Values explicitly specified.

    ```xml
    <IndividualValueSet startIndex="..." endIndex="...">
        <D>3.14</D>
        <I>42</I>
        ...
    </IndividualValueSet>
    ```

    Attributes:
        endIndex (int | None): Zero-based index of the last entry in this Value Set. The specification is inclusive.
        startIndex (int | None): Zero-based index of the first entry in this Value Set. The specification is inclusive.

        values (list[BooleanType | DoubleType | DateTimeType | EmbeddedXmlType | FloatType | IntType | LongType | \
            PNGType | StringType | SVGType]]): A set of Value elements.
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
