from ctypes import c_float, c_int32, c_int64
from dataclasses import dataclass, field
from datetime import datetime
from typing import Annotated, Optional

from ..core import TEXT, XmlModel
from .base import AnIMLDocBase

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


@dataclass
class BooleanType(XmlModel, regclass=AnIMLDocBase):

    value: Annotated[bool, TEXT(**SERIALIZE_BOOL)]
    tag: str = "Boolean"


@dataclass
class DoubleType(XmlModel, regclass=AnIMLDocBase):
    """Individual 64-bit floating point value."""

    value: Annotated[float, TEXT(**SERIALIZE_DOUBLE)] = field()
    tag: str = "D"


@dataclass
class DateTimeType(XmlModel, regclass=AnIMLDocBase):

    value: Annotated[datetime, TEXT(**SERIALIZE_DATETIME)] = field()
    tag: str = "DateTime"


@dataclass
class EmbeddedXmlType(XmlModel, regclass=AnIMLDocBase):

    value: Annotated[Optional[str], TEXT] = field()
    tag: str = "EmbeddedXML"


@dataclass
class FloatType(XmlModel, regclass=AnIMLDocBase):
    """Individual 32-bit floating point value."""

    value: Annotated[float, TEXT(**SERIALIZE_FLOAT)] = field()
    tag: str = "F"


@dataclass
class IntType(XmlModel, regclass=AnIMLDocBase):
    """Individual integer value (32 bits, signed)."""

    value: Annotated[int, TEXT(**SERIALIZE_INT)] = field()
    tag: str = "I"


@dataclass
class LongType(XmlModel, regclass=AnIMLDocBase):
    """Individual long integer value (64 bits, signed)."""

    value: Annotated[int, TEXT(**SERIALIZE_LONG)] = field()
    tag: str = "L"


@dataclass
class PNGType(XmlModel, regclass=AnIMLDocBase):

    value: Annotated[Optional[bytes], TEXT] = None
    tag: str = "PNG"


@dataclass
class StringType(XmlModel, regclass=AnIMLDocBase):

    value: Annotated[Optional[str], TEXT] = field()
    tag: str = "S"


@dataclass
class SVGType(XmlModel, regclass=AnIMLDocBase):

    value: Annotated[Optional[str], TEXT] = field()
    tag: str = "SVG"
