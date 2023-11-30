from __future__ import annotations

from xml.etree.ElementTree import Element

from pydantic import BaseModel


class XmlModel(BaseModel):
    """Base class to be used with AnIMLDoc sub models."""

    def dump_xml(self) -> Element:
        """Return an ElementTree Element representing the model."""
        # Default implementation
        me = Element(self.__class__.__name__)
        self._add_pydantic_fields(me)
        self._append_pydantic_children(me)
        return me

    @classmethod
    def load_xml(node: Element) -> XmlModel:
        """Return a pydantic model instance from an ElementTree Element."""
        raise NotImplementedError

    def _add_pydantic_fields(self, node: Element):
        fields = filter(
            lambda x: isinstance(x[1], (str, int, float)),
            [(k, getattr(self, k)) for k in self.model_fields],
        )
        for f in fields:
            node.attrib[f[0]] = str(f[1])

    def _append_pydantic_children(self, node: Element):
        """Append pydantic fields as children to an ElementTree Element."""
        fields = filter(
            lambda x: isinstance(x, (list, XmlModel)),
            [getattr(self, k) for k in self.model_fields],
        )
        for f in fields:
            if f is None:
                continue
            if isinstance(f, XmlModel):
                node.append(f.dump_xml())
            elif isinstance(f, list):
                for item in f:
                    if isinstance(item, XmlModel):
                        node.append(item.dump_xml())
                    else:
                        raise TypeError(f"Expected XmlModel, got {type(item)}")
            else:
                raise Exception(f"Big suss error - should never get here")
