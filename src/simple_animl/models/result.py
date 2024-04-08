from __future__ import annotations

from typing import List, Optional

from ..core import Field, XmlModel
from ..utils.regex import NC_NAME
from .base import AnIMLDocBase
from .category import Category
from .infrastructure import Infrastructure
from .method import Method
from .series import SeriesSet
from .tags import TagSet
from .techinque import Technique
from .template import Template


class ExperimentStep(XmlModel, regclass=AnIMLDocBase):
    # Attributes
    experimentStepID: str = Field.Attribute()
    name: str = Field.Attribute()
    comment: Optional[str] = Field.Attribute()
    id: Optional[str] = Field.Attribute(regex=NC_NAME)
    sourceDataLocation: Optional[str] = Field.Attribute()
    templateUsed: Optional[str] = Field.Attribute()

    # Children
    tag_set: Optional[TagSet] = Field.Child()
    technique: Optional[Technique] = Field.Child()
    infrastructure: Optional[Infrastructure] = Field.Child()
    method: Optional[Method] = Field.Child()
    result: Optional[list[Result]] = Field.Child()


class ExperimentStepSet(XmlModel, regclass=AnIMLDocBase):
    """
    Container for multiple ExperimentSteps that describe the process and results.

    Children:
        templates (optional(list(Template))): Collection of Templates
        experiment_steps (list(ExperimentStep)): Collection of ExperimentSteps
    """

    # Children
    templates: list[Template] = Field.Child(default_factory=list)
    experiment_steps: Optional[list[ExperimentStep]] = Field.Child(default_factory=list)


class Result(XmlModel, regclass=AnIMLDocBase):
    """
    Container for Data derived from Experiment.

    Attributes:
        id (str): Anchor point for digital signature. This identifier \
            is referred to from the "Reference" element in a Signature. Unique per document.
        name (str): Name of this Result

    Children:
        series (optional(SeriesSet)): Container for n-dimensional Data.
        category_set (list(Category)): Collection of Categories
        experiment_step (optional(ExperimentStepSet)): Container for multiple ExperimentSteps \
            that describe the process and results.

    """

    # Attributes
    id: Optional[str] = Field.Attribute(regex=NC_NAME)
    name: str = Field.Attribute()

    # Children
    series: Optional[SeriesSet] = Field.Child()
    category_set: List[Category] = Field.Child()
    experiment_step: Optional[ExperimentStepSet] = Field.Child()
