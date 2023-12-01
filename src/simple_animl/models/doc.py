from __future__ import annotations

from io import StringIO
from typing import IO, Optional, Union
from xml.etree.ElementTree import Element, ElementTree

from simple_animl.models.sample import Sample, SampleSet

from .core import XmlModel

VERSION: str = "0.90"
XMLNS: str = "urn:org:astm:animl:schema:core:draft:0.90"
XMLNS_XSI: str = "http://www.w3.org/2001/XMLSchema-instance"
XSI_SCHEMALOCATION: str = "urn:org:astm:animl:schema:core:draft:0.90 http://schemas.animl.org/current/animl-core.xsd"


class AnIMLDoc(XmlModel):
    """Root Element for AnIML documents."""

    sample_set: Optional[SampleSet] = None
    experiment_set: Optional[XmlModel] = None

    def add(self, obj: Sample):
        if isinstance(obj, Sample):
            if self.sample_set is None:
                self.sample_set = SampleSet()
            self.sample_set.samples.append(obj)
        else:
            raise TypeError(f"Expected Sample, got {type(obj)}")

    def dump_xml(self) -> Element:
        me = Element(
            "AnIML",
            attrib={
                "version": VERSION,
                "xmlns": XMLNS,
                "xmlns:xsi": XMLNS_XSI,
                "xsi:schemaLocation": XSI_SCHEMALOCATION,
            },
        )
        self._append_pydantic_children(me)
        self._add_pydantic_fields(me)
        return me

    @classmethod
    def loads(cls, xml: Union[IO, str]) -> AnIMLDoc:
        if isinstance(xml, str):
            xml = StringIO(xml)
        elif isinstance(xml, IO):
            pass  # Nothing
        else:
            raise TypeError(f"Expected str or IO, got {type(xml)}")
        et = ElementTree()
        et.parse(source=xml)
        return cls.load_xml(et.getroot())

    @classmethod
    def load_xml(cls, node: Element) -> XmlModel:
        if node is None:
            return None
        return cls(
            sample_set=SampleSet.load_xml(node.find("SampleSet")),
            experiment_set=None,
        )
