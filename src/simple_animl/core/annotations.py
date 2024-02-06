from __future__ import annotations

import re
from dataclasses import dataclass
from pydoc import locate
from typing import Any, Type, Union, _GenericAlias, _SpecialForm, _UnionGenericAlias


@dataclass
class Annotation:
    _type: Union[str, type]
    isOptional: bool
    isList: bool
    # TODO: Make class support more complex annotations

    __registered_types__ = {}

    def check_type_ex(self, value: Any, name: str):
        if value is None:
            if self.isOptional:
                return
            else:
                raise ValueError(f"Field '{name}' is not optional")

        def get_types():
            yield None if isinstance(self._type, str) else self._type
            yield locate(self._type)  # Use for built in types
            yield type(self).get_type_from_string(self._type)
            raise TypeError(f"Type '{self._type}' not found")

        for t in get_types():
            if t is None:
                continue
            if isinstance(value, t):
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
                f"Type mismatch. Expected: '{self._type}', got: '{type(value).__name__}'"
            )

    def validtype(self, type: Type):
        """Check if provided type is valid for this annotation"""
        return self._type == type or self._type == type.__name__

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

    @classmethod
    def register_type(cls, Type):
        if Type.__name__ in cls.__registered_types__:
            raise ValueError(f"Type '{Type.__name__}' already registered")
        cls.__registered_types__[Type.__name__] = Type

    @classmethod
    def get_type_from_string(cls, name) -> Union[Type, None]:
        return cls.__registered_types__.get(name, None)

    @classmethod
    def get_registered_types(cls) -> list[Type]:
        return list(cls.__registered_types__.values())


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
        isOptional = False
        isList = False
        if annotation.lower().startswith("optional["):
            isOptional = True
            annotation = annotation[9:-1]
            ret = Annotation.parse(annotation)
            ret.isList |= isList
            ret.isOptional |= isOptional
            return ret
        elif annotation.lower().startswith("list["):
            isList = True
            annotation = annotation[5:-1]
            ret = Annotation.parse(annotation)
            ret.isList |= isList
            ret.isOptional |= isOptional
            return ret
        elif not re.match(r"^[a-zA-Z0-9_]+$", annotation):  # Not a valid type name
            raise SyntaxError(f"Invalid type syntax: '{annotation}'")

        return Annotation(annotation, False, False)


class TypeAnnotation(BaseAnnotation):
    @classmethod
    def parse(cls, annotation: type) -> Annotation:
        """Parse a type-hint of python standard type"""
        isList = False
        if hasattr(annotation, "__origin__") and annotation.__origin__ == list:
            isList = True
            ret = Annotation.parse(annotation.__args__[0])
            ret.isList |= isList
            return ret
        else:
            return Annotation(annotation, False, False)


class TypingAnnotation(BaseAnnotation):
    @classmethod
    def parse(cls, annotation: _SpecialForm):
        """Parse a type-hint from the python 'typing' library"""
        if annotation.__module__ != "typing":
            raise TypeError(
                f"Type from module '{annotation.__module__}', expected to be from 'typing'"
            )
        isOptional = False
        isList = False
        if isinstance(annotation, _UnionGenericAlias):  # Union or Optional
            # Optional
            if len(annotation.__args__) == 2 and annotation.__args__[1] == type(None):
                annotation = annotation.__args__[0]
                isOptional = True
            else:
                raise TypeError(f"Unsupported typing type: '{str(annotation)}'")

        elif isinstance(annotation, _GenericAlias):  # Other type
            if annotation._name == "List":  # List
                annotation = annotation.__args__[0]
                isList = True
            else:
                raise TypeError(f"Unsupported typing type: '{str(annotation)}'")
        else:
            raise TypeError(f"Unsupported typing type: '{str(annotation)}'")
        ret = Annotation.parse(annotation)
        ret.isOptional |= isOptional
        ret.isList |= isList
        return ret
