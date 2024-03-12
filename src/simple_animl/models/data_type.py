from ctypes import c_float, c_int32, c_int64
from datetime import datetime
from typing import Optional, Union

from ..core.base import XmlModel
from ..core.fields import Field

SERIALIZE_BINARY = {
    "on_serialize": lambda x: x.decode("ascii") if x else None,
    "on_deserialize": lambda x: x.encode("ascii") if x else None,
}

# Need have it serialized as true/false, not True/False
SERIALIZE_BOOL = {
    "on_serialize": lambda x: "true" if x else "false",
    "on_deserialize": lambda x: x == "true",
}

SERIALIZE_DOUBLE = {
    "on_serialize": lambda x: f"{x}" if x is not None else None,
    "on_deserialize": lambda x: float(x) if x else None,
}


SERIALIZE_FLOAT = {
    "on_serialize": lambda x: f"{c_float(x).value}" if x is not None else None,
    "on_deserialize": lambda x: float(x) if x else None,
}

SERIALIZE_DATETIME = {
    "on_serialize": lambda x: x.isoformat() if x is not None else None,
    "on_deserialize": lambda x: datetime.fromisoformat(x) if x else None,
}

SERIALIZE_INT = {
    "on_serialize": lambda x: f"{c_int32(x).value}" if x is not None else None,
    "on_deserialize": lambda x: int(x) if x else None,
}

SERIALIZE_LONG = {
    "on_serialize": lambda x: f"{c_int64(x).value}" if x is not None else None,
    "on_deserialize": lambda x: int(x) if x else None,
}


class BooleanType(XmlModel):
    tag: str = "Boolean"

    value: bool = Field.Text(**SERIALIZE_BOOL)


class DoubleType(XmlModel):
    """Individual 64-bit floating point value."""

    tag: str = "D"

    value: float = Field.Text(**SERIALIZE_DOUBLE)


class DateTimeType(XmlModel):
    tag: str = "DateTime"

    value: datetime = Field.Text(**SERIALIZE_DATETIME)


class EmbeddedXmlType(XmlModel):
    tag: str = "EmbeddedXML"

    value: Optional[str] = Field.Text()


class FloatType(XmlModel):
    """Individual 32-bit floating point value."""

    tag: str = "F"

    value: float = Field.Text(**SERIALIZE_FLOAT)


class IntType(XmlModel):
    """Individual integer value (32 bits, signed)."""

    tag: str = "I"

    value: int = Field.Text(**SERIALIZE_INT)


class LongType(XmlModel):
    """Individual long integer value (64 bits, signed)."""

    tag: str = "L"

    value: int = Field.Text(**SERIALIZE_LONG)


class PNGType(XmlModel):
    tag: str = "PNG"

    value: Optional[bytes] = Field.Text()


class StringType(XmlModel):
    tag: str = "S"

    value: Optional[str] = Field.Text()


class SVGType(XmlModel):
    tag: str = "SVG"

    value: Optional[str] = Field.Text()
