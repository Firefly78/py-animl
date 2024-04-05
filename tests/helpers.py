from simple_animl.core.base import XmlDocBase


def create_dummy_regclass():
    """Each call to this function will return a new class that inherits from XmlDocBase."""

    class DummyBase(XmlDocBase):
        pass

    return DummyBase
