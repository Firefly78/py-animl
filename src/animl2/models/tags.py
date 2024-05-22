from __future__ import annotations

from dataclasses import dataclass, field
from typing import Annotated, Optional

from ..core import ATTRIB, CHILD, XmlModel
from .base import AnIMLDocBase


@dataclass
class Tag(XmlModel, regclass=AnIMLDocBase):
    """
    Tag to mark related data items. When a value is given, it may also serve as a reference to an external data system.

    Attributes:
        name (str): Token with up to 1024 characters
        value (str): String with up to 1024 characters

    """

    name: Annotated[str, ATTRIB]
    value: Annotated[Optional[str], ATTRIB]


@dataclass
class TagSet(XmlModel, regclass=AnIMLDocBase):
    """Set of Tag elements."""

    tags: Annotated[Optional[list[Tag]], CHILD] = field(default_factory=list)

    def append(self, tag: Tag):
        self.tags.append(tag)
        return tag
