from enum import Enum
from typing import List, Optional, Union

from ..core import Field, XmlModel
from ..utils.regex import NC_NAME
from .base import AnIMLDocBase
from .data_type import SERIALIZE_BOOL, SERIALIZE_INT
from .parameter import ParameterType
from .unit import Unit
from .valuesets import AutoIncrementedValueSet, EncodedValueSet, IndividualValueSet


class Dependency(str, Enum):
    Independent = "independent"
    Dependent = "dependent"


AnIMLDocBase.register(Dependency.__name__, Dependency)


class PlotScale(str, Enum):
    Linear = "linear"
    Ln = "ln"
    Log = "log"
    none = "none"


AnIMLDocBase.register(PlotScale.__name__, PlotScale)


class Series(XmlModel, regclass=AnIMLDocBase):
    """Container for multiple Values.

    Attributes:
        name (str): Plain-text name of this item.
        dependency (Dependency): Specified whether the Series is independent or dependent.
        id (str): Anchor point for digital signature. This identifier is referred to from the "Reference" \
              element in a Signature. Unique per document.
        plotScale (PlotScale): Specifies whether the data in this Series is typically plotted on a linear \
              or logarithmic scale.
        seriesID (str): Identifies the Series. Used in References from subordinate ExperimentSteps. Unique \
              per SeriesSet.
        seriesType (ParameterTypes): Data type used by all values in this Series.
        visible (bool): Specifies whether data in this Series is to be displayed to the user by default.

    Children:
        valuesets (list[AutoIncrementedValueSet | EncodedValueSet | IndividualValueSet]): A set of ValueSet elements.
        unit (Unit): The unit of measure for the data in this Series.
    """

    name: str = Field.Attribute()
    dependency: Dependency = Field.Attribute()
    id: Optional[str] = Field.Attribute(regex=NC_NAME)
    plotScale: Optional[PlotScale] = Field.Attribute()
    seriesID: str = Field.Attribute()
    seriesType: ParameterType = Field.Attribute()
    visible: Optional[bool] = Field.Attribute(**SERIALIZE_BOOL)

    valuesets: Optional[
        List[Union[AutoIncrementedValueSet, EncodedValueSet, IndividualValueSet]]
    ] = Field.Child()
    unit: Optional[Unit] = Field.Child()


class SeriesSet(XmlModel, regclass=AnIMLDocBase):
    """Container for n-dimensional Data.

    Attributes:
        name (str): Plain-text name of this item.
        id (str): Anchor point for digital signature. This identifier is referred to from the "Reference" \
            element in a Signature. Unique per document.
        length (int): Number of data points each Series contains.

    Children:
        series (list[Series]): A set of Series elements.

    """

    name: str = Field.Attribute()
    id: Optional[str] = Field.Attribute(regex=NC_NAME)
    length: int = Field.Attribute(**SERIALIZE_INT)

    series: list[Series] = Field.Child()
