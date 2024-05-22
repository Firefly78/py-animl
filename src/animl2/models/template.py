from dataclasses import dataclass

from ..core.base import XmlModel
from .base import AnIMLDocBase


@dataclass
class Template(XmlModel, regclass=AnIMLDocBase):
    pass
