import xml.etree.ElementTree as ET

from animl2.core.base import XmlDocBase


def create_dummy_regclass():
    """Each call to this function will return a new class that inherits from XmlDocBase."""

    class DummyBase(XmlDocBase):
        pass

    return DummyBase


def make_element(tag, *, attrib={}, text=None, children=None):
    """Create an ElementTree element with the given tag, attributes, text, and children."""

    element = ET.Element(tag, attrib)
    if text is not None:
        element.text = text
    if children is not None:
        for child in children:
            element.append(child)
    return element
