from ..core import Field, XmlModel
from .base import AnIMLDocBase


class Name(XmlModel, regclass=AnIMLDocBase):
    """
    Common name.

    Text:
        value (str): Name value

    """

    # Text
    value: str = Field.Text()


class Manufacturer(XmlModel, regclass=AnIMLDocBase):
    """
    Company name.

    Text:
        value (str): Manufacturer value
    """

    # Text
    value: str = Field.Text()
