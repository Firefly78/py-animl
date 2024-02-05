import re
from typing import Any, Union, _SpecialForm

from .annotations import Annotation


class Field:
    """Container class for field types.

    Ment to create a clearer syntax when using the contained classes.

    ```python
    Class MyModel(XmlModel):
      name: str = Field.Attribute()
      # name: str = Attribute() - Not as clear
      value: str = Field.Attribute()
    ```
    """

    class Base:
        """Base-Field class. Not to be used directly."""

        def __init__(
            self,
            *,
            default=None,
            default_factory=None,
            on_serialize=None,
            on_deserialize=None,
            regex=None,
        ) -> None:
            if type(self) is Field.Base:
                raise ("Field.Base cannot be directly instantiated")
            self.default = default
            self.default_factory = default_factory
            self.on_serialize = on_serialize
            self.on_deserialize = on_deserialize
            self.regex = regex

            self.annotation: Annotation = None
            self.name: str = None

        def deserialize(self, value: Any) -> Any:
            if self.on_deserialize is not None:
                return self.on_deserialize(value)
            return value

        def get_default(self):
            if self.default is not None:
                return self.default
            elif self.default_factory is not None:
                return self.default_factory()
            else:
                return None

        def has_default(self):
            return self.default is not None or self.default_factory is not None

        def serialize(self, value: Any) -> Any:
            if self.on_serialize is not None:
                return self.on_serialize(value)
            return value

        def validate_ex(self, value: Any) -> Any:
            # Regex
            if self.regex is not None:
                if not re.match(self.regex, value):
                    raise ValueError(f"{self.name} must match regex {self.regex}")

            # Add more checks here...

            # Return value if all is good
            return value

    class Attribute(Base):
        """Attribute-Field class. Used to define attributes in XmlModel.

        ```python
        class MyModel(XmlModel):
            spam: str = Field.Attribute(default="my-spam")
        ```

        => `<MyModel spam="my-spam" />`

        Args:
            alias (str): Alias for attribute, used when serializing to xml.
            default (str): Default value for attribute, used if no value is provided.
            default_factory (function): Function that returns a default value for attribute, used if no value is provided.
            on_serialize (function): Function that is called when serializing the attribute to xml.
            on_deserialize (function): Function that is called when deserializing the attribute from xml.
            regex (str): Regular expression that the attribute must match.
        """

        def __init__(self, *, alias: str = None, **kwargs) -> None:
            if alias is not None and not isinstance(alias, str):
                raise TypeError("alias must be a string or None")
            super().__init__(**kwargs)
            self.alias = alias

    class Child(Base):
        """Child-Field class. Used to define xml child elements in XmlModel.

        ```python
        class MyModel(XmlModel):
            chilren: TestModel = Field.Child(default_factory=TestModel)
        ```

        => `<MyModel> <TestModel /> </MyModel>`

        Args:
            default (XmlModel): Default value for child element, used if no value is provided.
            default_factory (function): Function that returns a default value for child element, used if no value is provided.
        """

        def __init__(self, **kwargs) -> None:
            super().__init__(**kwargs)

    class Text(Base):
        """Text-Field class. Used to define the text content in a XmlModel element.

        ```python
        class MyModel(XmlModel):
            content: str = Field.Text(default="my text content")
        ```

        => `<MyModel>my text content</MyModel>`

        Args:
            default (str | type[Enum]): Default value for text content, used if no value is provided.
            default_factory (function): Function that returns a default value for text content, used if no value is provided.
            on_serialize (function): Function that is called when serializing the attribute to xml.
            on_deserialize (function): Function that is called when deserializing the attribute from xml.
            regex (str): Regular expression that the text must match.
        """

        def __init__(self, **kwargs) -> None:
            super().__init__(**kwargs)
