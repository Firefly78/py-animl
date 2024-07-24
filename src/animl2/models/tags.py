from __future__ import annotations

from dataclasses import dataclass, field
from typing import Annotated, Optional, overload

from ..core import ATTRIB, CHILD, XmlModel
from .base import AnIMLDocBase


@dataclass
class Tag(XmlModel, regclass=AnIMLDocBase):
    """
    Tag to mark related data items. When a value is given, it may also serve as a reference to an external data system.

    ```xml
    <Tag name="..." value="..."/>

    ```

    Attributes:
        name (str): Token with up to 1024 characters
        value (str | None): String with up to 1024 characters

    """

    name: Annotated[str, ATTRIB]
    value: Annotated[Optional[str], ATTRIB]


@dataclass
class TagSet(XmlModel, regclass=AnIMLDocBase):
    """
    Set of Tag elements.

    ```xml
    <TagSet>
        <Tag name="..." value="..."/>
    </TagSet>
    ```

    Attributes:
        tags (list[Tag] | None): List of Tag elements


    """

    tags: Annotated[Optional[list[Tag]], CHILD] = field(default_factory=list)

    @overload
    def append(self, item: Tag) -> Tag:
        """Add a Tag to this TagSet"""

    def append(self, item):
        self.tags.append(item)
        return item
