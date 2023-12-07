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

        def __init__(self, default=None, default_factory=None) -> None:
            if type(self) is Field.Base:
                raise TypeError("Field.Base cannot be directly instantiated")
            self.default = default
            self.default_factory = default_factory
            self.optional = False

        def get_default(self):
            if self.default is not None:
                return self.default
            elif self.default_factory is not None:
                return self.default_factory()
            else:
                return None

        def set_annotation(self, annotation: str):
            if annotation is None:
                raise TypeError("Annotation must be specified")

            if annotation.startswith("Optional["):
                self.annotation = annotation[9:-1]
                self.optional = True
            else:
                self.annotation = annotation
            return self

    class Attribute(Base):
        def __init__(
            self, default=None, default_factory=None, alias: str = None
        ) -> None:
            super().__init__(default, default_factory)
            self.alias = alias

        def set_annotation(self, annotation: str):
            super().set_annotation(annotation)
            if self.annotation != "str":
                raise TypeError(f"Invalid annotation '{self.annotation}'")
            return self

    class Child(Base):
        def __init__(self, index=-1, default=None, default_factory=None) -> None:
            super().__init__(default=default, default_factory=default_factory)
            self.index = index  # Index defines order in which fields are serialized to xml - not implemented
            self.isList = False

        def set_annotation(self, annotation: str):
            super().set_annotation(annotation)
            if annotation.lower().startswith("list["):
                self.annotation = annotation[5:-1]
                self.isList = True
            return self

    class Text(Base):
        pass
