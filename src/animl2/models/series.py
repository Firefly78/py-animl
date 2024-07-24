from dataclasses import dataclass, field
from enum import Enum
from typing import Annotated, List, Optional, Union

from ..core import ATTRIB, CHILD, XmlModel
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


@dataclass
class Series(XmlModel, regclass=AnIMLDocBase):
    """Container for multiple Values.

    ```xml
    <Series name="..." dependency="..." id="..." plotScale="..." seriesID="..." seriesType="..." visible="...">
        <ValueSet .../>
        <Unit .../>
    </Series>

    Attributes:
        name (str): Plain-text name of this item.
        dependency (Dependency): Specified whether the Series is independent or dependent.
        id (str | None): Anchor point for digital signature. This identifier is referred to from the "Reference" \
              element in a Signature. Unique per document.
        plotScale (PlotScale | None): Specifies whether the data in this Series is typically plotted on a linear \
              or logarithmic scale.
        seriesID (str): Identifies the Series. Used in References from subordinate ExperimentSteps. Unique \
              per SeriesSet.
        seriesType (ParameterTypes): Data type used by all values in this Series.
        visible (bool | None): Specifies whether data in this Series is to be displayed to the user by default.

        valuesets (list[AutoIncrementedValueSet | EncodedValueSet | IndividualValueSet]): A set of ValueSet elements.
        unit (Unit): The unit of measure for the data in this Series.
    """

    name: Annotated[str, ATTRIB]
    dependency: Annotated[Dependency, ATTRIB]
    id: Annotated[Optional[str], ATTRIB(regex=NC_NAME)]
    plotScale: Annotated[Optional[PlotScale], ATTRIB]
    seriesID: Annotated[str, ATTRIB]
    seriesType: Annotated[ParameterType, ATTRIB]
    visible: Annotated[Optional[bool], ATTRIB(**SERIALIZE_BOOL)] = None

    valuesets: Annotated[
        List[Union[AutoIncrementedValueSet, EncodedValueSet, IndividualValueSet]],
        CHILD,
    ] = field(default_factory=list)
    unit: Annotated[Optional[Unit], CHILD] = None


@dataclass
class SeriesSet(XmlModel, regclass=AnIMLDocBase):
    """Container for n-dimensional Data.

    ```xml
    <SeriesSet name="..." id="..." length="...">
        <Series .../>
        <Series .../>
        ...
    </SeriesSet>
    ```

    Attributes:
        name (str): Plain-text name of this item.
        id (str | None): Anchor point for digital signature. This identifier is referred to from the "Reference" \
            element in a Signature. Unique per document.
        length (int): Number of data points each Series contains.

        series (list[Series]): A set of Series elements.
    """

    name: Annotated[str, ATTRIB]
    id: Annotated[Optional[str], ATTRIB(regex=NC_NAME)]
    length: Annotated[int, ATTRIB(**SERIALIZE_INT)]

    series: Annotated[list[Series], CHILD]
