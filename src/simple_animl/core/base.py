from __future__ import annotations

import logging
from typing import Any
from xml.etree import ElementTree as ET

from .fields import Field

logger = logging.getLogger(__name__)


class XmlModel:
    tag: str = None  # Override in subclass if tag is different from class name

    def __init__(self, **kwargs) -> None:
        self._init_tag_()
        self._init_model_()
        self._init_fields_(kwargs)

    def _init_fields_(self, kwargs: dict[str, Any]):
        for k in self._model_attributes:
            setattr(self, k, getattr(self, k).get_default())
        for k in self._model_children:
            setattr(self, k, getattr(self, k).get_default())
        for k in self._model_text:
            setattr(self, k, getattr(self, k).get_default())

        for k, v in kwargs.items():
            if k in self._model_attributes:
                setattr(self, k, v)
            elif k in self._model_children:
                setattr(self, k, v)
            elif k in self._model_text:
                setattr(self, k, v)
            else:
                KeyError(f"Invalid parameter: '{k}'")

    def _init_model_(self):
        self._model_attributes: dict[str, Field.Attribute] = {}
        self._model_children: dict[str, Field.Child] = {}
        self._model_text: dict[str, Field.Text] = {}
        A = self.__annotations__
        for name, annotation in A.items():
            try:
                attr = getattr(self.__class__, name)
            except AttributeError:
                continue  # not initiated field - ok
            if isinstance(attr, Field.Attribute):
                self._model_attributes[name] = attr.set_annotation(annotation)
            elif isinstance(attr, Field.Child):
                self._model_children[name] = attr.set_annotation(annotation)
            elif isinstance(attr, Field.Text):
                self._model_text[name] = attr.set_annotation(annotation)
            else:
                pass  # Not part of model - ok

    def _init_tag_(self):
        if self.tag is None:
            self.tag = self.__class__.__name__

    @classmethod
    def _get_type_from_tag_(cls, tag: str) -> type[XmlModel]:
        L = list(
            filter(
                lambda x: x.tag == tag or x.__name__ == tag,
                XmlModel.__subclasses__(),
            )
        )
        if len(L) == 0:
            raise ValueError(f"Unable to find class with name '{tag}'")
        elif len(L) > 1:
            raise ValueError(f"Multiple classes with name '{tag}'")
        else:
            return L[0]

    def dump_xml(self) -> ET.Element:
        x = ET.Element(self.tag)

        # Dump attributes
        x.attrib = {
            field.alias if field.alias is not None else name: getattr(self, name)
            for name, field in self._model_attributes.items()
            if getattr(self, name) is not None
        }

        # Dump text
        if self._model_text:
            x.text = self._model_text[0]

        # Dump children
        for name in self._model_children.keys():
            try:
                model = getattr(self, name)
            except AttributeError:
                continue
            if model is None:
                continue
            if isinstance(model, list):
                for i in model:
                    if isinstance(i, XmlModel):
                        x.append(i.dump_xml())
                    else:
                        raise TypeError
            elif isinstance(model, XmlModel):
                x.append(model.dump_xml())
            else:
                raise TypeError

        return x

    @classmethod
    def load_xml(cls, x: ET.Element) -> XmlModel:
        if x.tag != cls.tag and x.tag != cls.__name__:
            raise ValueError(f"Expected tag '{cls.tag}', got '{x.tag}'")
        model = cls()

        # Load attributes
        # TODO: Check that no additional fields are present
        for name, field in model._model_attributes.items():
            # Replace name with alias if present
            name = field.alias if field.alias is not None else name

            if field.optional:
                if name not in x.attrib:
                    continue  # Skip optional fields that are not present

            if name not in x.attrib:
                raise ValueError(f"Missing attribute '{name}'")
            setattr(model, name, x.attrib[name])

        # Load text
        # TODO: Check that text is not present if not allowed
        for name, field in model._model_text.items():
            if x.text is None:
                logger.warning(f"Missing text for field '{name}'")
            setattr(model, model._model_text[0], x.text)
            break  # Only one text field allowed

        # Load children
        for child in x:
            # Create child instance from xml
            child_instance = cls._get_type_from_tag_(child.tag).load_xml(child)
            # Find someplace to store it...
            a = list(
                filter(
                    lambda x: x[1].annotation == child_instance.__class__.__name__,
                    model._model_children.items(),
                )
            )
            if len(a) == 0:
                raise ValueError(f"Unable to find field for child '{child.tag}'")
            if len(a) > 1:
                raise ValueError(f"Multiple fields for child '{child.tag}'")
            name, field = a[0]

            if field.isList:
                if getattr(model, name) is None:  # List if None
                    setattr(model, name, list())
                getattr(model, name).append(child_instance)
            else:
                setattr(model, name, child_instance)

        return model
