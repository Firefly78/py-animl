from __future__ import annotations

import logging
from copy import copy
from enum import Enum
from typing import Any, overload
from xml.etree import ElementTree as ET

from .annotations import Annotation
from .fields import Field

logger = logging.getLogger(__name__)


class XmlMeta(type):
    """Meta class used to evaluate fields on class definition"""

    def __new__(
        cls,
        name: str,
        bases: tuple[type],
        attrs: dict[str, Any],
        regclass: type[XmlDocBase] = None,
    ):
        """Called when a new class is defined"""
        # If model name is XmlModel - just define it and return
        # It is not possible to access the 'XmlModel' type - since it is not yet defined
        # Note to self: super().__new__ has side effects, make sure it is never run twice!
        if attrs["__module__"] == __name__ and name == "XmlModel":
            return super().__new__(cls, name, bases, attrs)  # Just return (Do nothing)

        # Check that XmlDocBase was not used instead of XmlModel
        if (
            attrs["__module__"] == __name__ and name == "XmlDocBase"
        ) or XmlDocBase in bases:
            raise TypeError("XmlDocBase should not be used with RegXmlMeta metaclass")

        # Check that created class is a subclass of XmlModel
        if XmlModel not in bases:
            raise TypeError(f"Only XmlModel can be used with XmlMeta not '{name}'")

        # Enforce use of regclass
        if regclass is None:
            raise ValueError("Regclass must be provided")

        # Check that regclass is a subclass of XmlDocBase
        if not issubclass(regclass, XmlDocBase):
            raise TypeError("Regclass class is not a subclass of XmlDocBase")

        # Extract fields and tag details
        fields = cls.extract_fields(attrs)
        tag = cls.get_tag(name, attrs)

        # Update static attributes
        attrs["_fields"] = fields
        attrs["tag"] = tag

        cls.check_restrictions(fields)

        new_type: XmlModel = super().__new__(cls, name, bases, attrs)
        regclass.register(tag, new_type)  # Register class
        new_type.assign_regclass(regclass)  # Assign lookup class
        return new_type

    @classmethod
    def check_restrictions(cls, fields: list[Field.Base]):
        """Check that the model follows all restrictions"""

        # Check that there is at most one text field
        if len(list(filter(lambda x: isinstance(x, Field.Text), fields))) > 1:
            raise TypeError("Only one text field allowed")

    @classmethod
    def extract_fields(cls, attrs: dict[str, Any]) -> list[Field.Base]:
        """Extracts details on how an object's/model's fields are to be serialized"""

        # Extract annotation information from attrs
        annotation_lookup: dict[str, Any] = attrs.get("__annotations__", {})

        def _get_field(attr_name: str, value: Field.Base):
            # Check if annotation is available
            if attr_name not in annotation_lookup:
                raise TypeError(f"Field missing annotation: '{attr_name}'")

            value.name = attr_name  # Record field name
            value.annotation = Annotation.parse(annotation_lookup[attr_name])  # Magic
            return value

        # Run get_field on all attributes with content of type Field.Base
        return [_get_field(n, v) for n, v in attrs.items() if isinstance(v, Field.Base)]

    @classmethod
    def get_tag(cls, name: str, attrs: dict[str, Any]):
        """Get the XML tag to match this model to"""

        # If user has not provided an overwrite
        if "tag" not in attrs or attrs["tag"] is None:
            return name  # Use default
        return attrs["tag"]  # Otherwise - use user provided one.


class XmlDocBase:
    """Base class for registering XmlModel classes for deserialization"""

    @classmethod
    def get_registered_types(cls):
        """Get all registered types"""
        if not hasattr(cls, "_static_dict"):
            cls._static_dict: dict[str, type] = {}
        return cls._static_dict.copy()

    @classmethod
    def register(cls, key, value):
        """Register a type for deserialization"""
        if cls is XmlModel:
            raise TypeError("Cannot register on base class")
        if not hasattr(cls, "_static_dict"):
            cls._static_dict = {}
        # if cls.__name__ == "key":
        #    return
        if key in cls._static_dict:
            raise ValueError(f"Type '{key}' already registered")
        cls._static_dict[key] = value


class XmlModel(metaclass=XmlMeta):
    """Base class used to serialize/deserialize models to/from XML

    Args:
        tag (str): Element tag to use when serializing this model, if None will use class name
        _fields (list[Field.Base]): List of all serializable fields (attributes, children, text)
    """

    tag: str = None  # Override in subclass if tag is different from class name

    _fields: list[Field.Base] = list()

    def __init__(self, **kwargs) -> None:
        """Default constructor, makes sure all fields are set to default or provided values"""
        self._init_fields_(**kwargs)

    def _init_fields_(self, **kwargs):
        """Helper function for initializing fields"""
        kwargs = copy(kwargs)

        # Set all fields to provided or default values
        for i in self._fields:  # All fields
            key = (
                i.alias
                if isinstance(i, Field.Attribute) and i.alias is not None
                else i.name
            )
            if (
                key not in kwargs
                and not i.annotation.isOptional
                and not i.has_default()
            ):
                raise KeyError(f"Missing parameter: '{key}'")

            value = kwargs[key] if key in kwargs else i.get_default()
            i.annotation.check_type_ex(
                value, i.name, registered_types=type(self).get_registered_types()
            )  # Type check
            if value is not None:  # None check is handled by .annotation.check_type_ex
                i.validate_ex(value)  # Field validation
            setattr(self, i.name, value)

    @overload
    @classmethod
    def _get_fields_(cls, mask: type[Field.Attribute] = None) -> list[Field.Attribute]:
        ...

    @overload
    @classmethod
    def _get_fields_(cls, mask: type[Field.Child] = None) -> list[Field.Child]:
        ...

    @overload
    @classmethod
    def _get_fields_(cls, mask: type[Field.Text] = None) -> list[Field.Text]:
        ...

    @classmethod
    def _get_fields_(cls, mask=None):
        """Helper function for getting fields of a specific type"""
        if mask is None:
            return cls._fields
        return list(filter(lambda x: isinstance(x, mask), cls._fields))

    def dump_xml(self) -> ET.Element:
        """Dump this model and its children to an XML etree object"""
        x = ET.Element(self.tag)

        # Dump attributes
        x.attrib = self._dump_xml_attributes_()

        # Dump text
        x.text = self._dump_xml_text_()

        # Dump children
        x.extend(self._dump_xml_children_())

        return x

    def _dump_xml_attributes_(self):
        """Helper function for dumping attributes to XML"""
        return {
            field.get_name(): (
                field.validate_ex(field.serialize(getattr(self, field.name)))
            )
            for field in type(self)._get_fields_(Field.Attribute)
            if getattr(self, field.name) is not None
        }

    def _dump_xml_children_(self) -> list[ET.Element]:
        """Helper function for dumping children to XML"""
        items = []

        for field in type(self)._get_fields_(Field.Child):
            try:
                model = field.validate_ex(getattr(self, field.name))
            except AttributeError:
                continue
            if model is None:
                continue
            if isinstance(model, list):
                for i in model:
                    if isinstance(i, XmlModel):
                        items.append(i.dump_xml())
                    else:
                        raise TypeError
            elif isinstance(model, XmlModel):
                items.append(model.dump_xml())
            else:
                raise TypeError

        return items

    def _dump_xml_text_(self):
        """Helper function for dumping text content to XML"""
        try:
            text = type(self)._get_fields_(Field.Text)[0]  # There can be only one
        except IndexError:
            text = None

        if text is not None:  # There is a text field
            t = text.validate_ex(text.serialize(getattr(self, text.name)))

            # Check for None
            if t is None:
                if text.annotation.isOptional:  # Optional field
                    return None
                raise Exception(f"Text field '{text.name}' is missing")

            # Check type
            if not isinstance(t, str):
                raise TypeError(f"Text field '{text.name}' type must be string")

            # Handle enums
            if isinstance(t, Enum):
                if not isinstance(t.value, str):  # Check if also string
                    raise TypeError(f"Enum value must be string")
                return t.value  # Return value of enum i.e. string

            return t

        return None

    @classmethod
    def load_xml(cls, x: ET.Element):
        """Create an XmlModel from an XML etree object"""
        # Check matching tag
        if x.tag != cls.tag:
            raise ValueError(f"Expected tag '{cls.tag}', got '{x.tag}'")

        # Create arguments list
        arguments = {}

        # Load attributes
        arguments.update(cls._load_xml_attributes_(x))

        # Load text
        arguments.update(cls._load_xml_text_(x))

        # Load children
        arguments.update(cls._load_xml_children_(x))

        # Create instance and return
        return cls(**arguments)

    @classmethod
    def _load_xml_attributes_(cls, x: ET.Element):
        """
        Helper function for loading attributes from XML

        Args:
            x (ET.Element): XML Element to load attributes from
        """
        arguments = {}

        # TODO: Check that no additional fields are present
        for attr in cls._get_fields_(Field.Attribute):
            # Replace name with alias if present
            name = attr.alias if attr.alias is not None else attr.name

            if attr.annotation.isOptional:
                if name not in x.attrib:
                    continue  # Skip optional fields that are not present

            if name not in x.attrib:
                raise ValueError(f"Missing attribute '{name}'")

            arguments[name] = attr.validate_ex(attr.deserialize(x.attrib[name]))

        return arguments

    @classmethod
    def _load_xml_children_(cls, x: ET.Element):
        """
        Helper function for loading children from XML

        Args:
            x (ET.Element): XML Element to load children from
        """
        arguments = {}

        child_fields = cls._get_fields_(Field.Child)
        for child in x:
            # Create child instance from xml
            child_inst = cls.class_from_tag(child.tag).load_xml(child)

            # Find a field that matches the child
            a = [x for x in child_fields if x.annotation.validcontent(type(child_inst))]

            if len(a) > 1:
                # Check if any but the last is lists -> error
                if any([x.annotation.isList for x in a[:-1]]):
                    raise ValueError(f"Unreachable field found for child '{child.tag}'")
                # Check which ones are occupied (in arguments), and filter a
                a = [x for x in a if x.name not in arguments]
            if len(a) == 0:
                raise ValueError(f"Unable to find field for child '{child.tag}'")

            child_field = a[0]

            if child_field.annotation.isList:
                if child_field.name not in arguments:  # No list found
                    arguments[child_field.name] = list()
                arguments[child_field.name].append(child_inst)
            else:
                arguments[child_field.name] = child_inst

        return arguments

    @classmethod
    def _load_xml_text_(cls, x: ET.Element):
        """
        Helper function for loading text from XML

        Args:
            x (ET.Element): XML Element to load text from
        """
        arguments = {}

        # TODO: Check that text is not present if not allowed
        try:
            txt = cls._get_fields_(Field.Text)[0]
        except IndexError:
            return arguments

        if x.text is None and not txt.annotation.isOptional:
            raise ValueError(f"Missing required text field '{txt.name}'")

        arguments[txt.name] = txt.validate_ex(txt.deserialize(x.text))

        return arguments

    @classmethod
    def assign_regclass(cls, regclass: type[XmlDocBase]):
        """Assign the regclass for this model"""
        cls.regclass = regclass

    @classmethod
    def get_registered_types(cls):
        """Get all registered types"""
        return cls.regclass.get_registered_types()

    @classmethod
    def class_from_tag(cls, tag: str):
        """Helper function for getting an XmlModel subclass from a name-string"""

        all_models = cls.get_registered_types().values()
        L = list(filter(lambda x: issubclass(x, XmlModel) and x.tag == tag, all_models))

        if len(L) == 0:
            raise ValueError(f"Unable to find class with tag '{tag}'")
        elif len(L) > 1:
            raise ValueError(f"Multiple classes with tag '{tag}'")
        else:
            return L[0]
