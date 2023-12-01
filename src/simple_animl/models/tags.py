from __future__ import annotations

from typing import Optional
from xml.etree.ElementTree import Element

from pydantic import Field

from .core import XmlModel


class Tag(XmlModel):
    """Tag to mark related data items. When a value is given, it may also serve as a reference to an external data system."""

    name: str = Field(..., description="Token with up to 1024 characters")
    value: str = Field(..., description="Token with up to 1024 characters")

    @classmethod
    def load_xml(cls, node: Element) -> Tag:
        if node is None:
            return None
        return cls(
            name=node.attrib.get("name"),
            value=node.attrib.get("value"),
        )


class TagSet(XmlModel):
    tags: Optional[list[Tag]] = Field(default_factory=list)

    @classmethod
    def load_xml(cls, node: Element) -> TagSet:
        if node is None:
            return None
        return cls(
            tags=[Tag.load_xml(n) for n in node.findall("Tag")],
        )
