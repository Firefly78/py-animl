from __future__ import annotations

from typing import Optional
from xml.etree.ElementTree import Element

from .core import Field, XmlModel


class Tag(XmlModel):
    """
    Tag to mark related data items. When a value is given, it may also serve as a reference to an external data system.

    Args:
        name (str): Token with up to 1024 characters
        value (str): Token with up to 1024 characters

    """

    name: str = Field.Attribute()
    value: str = Field.Attribute()


class TagSet(XmlModel):
    """Set of Tag elements."""

    tags: Optional[list[Tag]] = Field.Child(default_factory=list)
