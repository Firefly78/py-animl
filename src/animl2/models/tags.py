from __future__ import annotations

from typing import Optional

from ..core import Field, XmlModel
from .base import AnIMLDocBase


class Tag(XmlModel, regclass=AnIMLDocBase):
    """
    Tag to mark related data items. When a value is given, it may also serve as a reference to an external data system.

    Attributes:
        name (str): Token with up to 1024 characters
        value (str): String with up to 1024 characters

    """

    name: str = Field.Attribute()
    value: Optional[str] = Field.Attribute()


class TagSet(XmlModel, regclass=AnIMLDocBase):
    """Set of Tag elements."""

    tags: Optional[list[Tag]] = Field.Child(default_factory=list)
