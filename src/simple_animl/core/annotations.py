from __future__ import annotations

import re
from dataclasses import dataclass
from pydoc import locate
from typing import Any, Type, Union, _GenericAlias, _SpecialForm, _UnionGenericAlias

NoneType = type(None)


@dataclass
class Annotation:
    tType: Union[str, type, None]
    subType: tuple[Union[Annotation, None], ...] = tuple()

    @property
    def isList(self):
        return self.validtype(list)

    def isOptional(self):
        return self.tType == Union and NoneType in self.subType

    __registered_types__ = {}

    def all_types(self):
        if self.tType == Union:
            re = []
            for t in self.subType:
                re.extend(t.all_types())
            return re
        return [self.tType]

    def check_type_ex(self, value: Any, name: str, registered_types: dict[str, Type]):
        """Check if provided value is valid for this annotation, if not raise an exception"""
        if value is None and not self.isOptional:
            raise ValueError(f"Field '{name}' is not optional")
        if value is None:
            return  # No value is ok

        def get_types():
            all_types = self.all_types()
            for t in all_types:
                yield None if isinstance(t, str) else t  # Not string
            for t in all_types:
                yield registered_types.get(t)
            for t in all_types:
                yield locate(t)  # Use for built in types
            # raise TypeError(f"Type '{self.tType}' not found")

        # self can be a range of types
        # Need check if any can be created from the value

        for t in get_types():
            if t is None:
                continue
            if isinstance(value, t):  # Matching type
                return
            if isinstance(value, list) and self.isList:
                return
            try:
                t(value)  # Try to convert
                return  # Conversion successful
            except ValueError as ex:
                raise
            except Exception as ex:
                pass

        raise TypeError(
            f"Type mismatch. Expected: '{self.tType}', got: '{type(value).__name__}'"
        )

    def validsubtype(self, type: Type):
        """Check if provided type is a valid subtype for this annotation, special case for List types"""
        if self.tType == Union and self.validtype(NoneType):
            return any([t.validsubtype(type) for t in self.subType])
        if self.tType == list:
            return any([t.validtype(type) for t in self.subType])
        return self.validtype(type)

    def validtype(self, type: Type):
        """Check if provided type is valid for this annotation"""
        if type is None:
            type = NoneType
        if self.tType == Union:
            return any([t.validtype(type) for t in self.subType])
        return self.tType == type or self.tType == type.__name__

    def validcontent(self, type: Type):
        """Check if provided type is valid for this annotation, including subtypes of a list"""
        return self.validtype(type) or (self.isList and self.validsubtype(type))

    @classmethod
    def parse(cls, annotation: Any) -> Annotation:
        """Create Annotation object from any type hint"""

        def _parse(annotation: str, target: type[BaseAnnotation]):
            return target.parse(annotation)

        # Check type-hint type and call matching constructor
        if isinstance(annotation, str):  # Check if string
            return _parse(annotation, target=StringAnnotation)
        elif isinstance(annotation, type):  # Check if python type
            return _parse(annotation, target=TypeAnnotation)
        elif annotation.__module__ == "typing":  # Check if typing.xx object
            return _parse(annotation, target=TypingAnnotation)
        else:
            raise TypeError


class BaseAnnotation:
    """Annotation parser base class"""

    @staticmethod
    def parse(annotation) -> Annotation:
        raise NotImplementedError


class StringAnnotation(BaseAnnotation):
    @classmethod
    def parse(cls, annotation: str) -> Annotation:
        """Parse a type-hint of type 'str'"""
        if not isinstance(annotation, str):
            raise TypeError(f"Parameter 'annotation': '{type(annotation)}'")
        if annotation.lower().startswith("optional["):
            annotation = annotation[9:-1]
            return Annotation(
                Union, (Annotation.parse(annotation), Annotation(NoneType))
            )
        elif annotation.lower().startswith("list["):
            annotation = annotation[5:-1]
            return Annotation(list, (Annotation.parse(annotation),))
        elif annotation.lower().startswith("union["):
            annotation = annotation[6:-1]
            types = annotation.split(", ")
            return Annotation(Union, tuple(map(Annotation.parse, types)))
        elif not re.match(r"^[a-zA-Z0-9_]+$", annotation):  # Not a valid type name
            raise SyntaxError(f"Invalid type syntax: '{annotation}'")
        else:
            return Annotation(annotation)


class TypeAnnotation(BaseAnnotation):
    @classmethod
    def parse(cls, annotation: type) -> Annotation:
        """Parse a type-hint of python standard type"""
        if hasattr(annotation, "__origin__") and annotation.__origin__ == list:
            return Annotation(list, (Annotation.parse(annotation.__args__[0]),))
        else:
            return Annotation(annotation)


class TypingAnnotation(BaseAnnotation):
    @classmethod
    def parse(cls, annotation: _SpecialForm):
        """Parse a type-hint from the python 'typing' library"""
        if annotation.__module__ != "typing":
            raise TypeError(
                f"Type from module '{annotation.__module__}', expected to be from 'typing'"
            )

        if isinstance(annotation, _UnionGenericAlias):  # Union or Optional
            return Annotation(
                Union,
                tuple(map(Annotation.parse, annotation.__args__)),
            )

        elif isinstance(annotation, _GenericAlias):  # Other type
            if annotation._name == "List":  # List
                return Annotation(list, (Annotation.parse(annotation.__args__[0]),))

        raise TypeError(f"Unsupported typing type: '{str(annotation)}'")
