from __future__ import annotations

from dataclasses import dataclass, field
from typing import Annotated, List, Optional

from ..core import ATTRIB, CHILD, XmlModel
from ..utils.regex import NC_NAME
from .base import AnIMLDocBase
from .category import Category
from .infrastructure import Infrastructure
from .method import Method
from .series import SeriesSet
from .tags import TagSet
from .technique import Technique


@dataclass
class ExperimentStep(XmlModel, regclass=AnIMLDocBase):
    """
    Container that documents a step in an experiment. Use one ExperimentStep \
        per application of a Technique.

    Attributes:
        experimentStepID (str): Unique identifier for this ExperimentStep. Used to \
            point to this step from an ExperimentDataReference.
        name (str): Plain-text name of this item.
        comment (str): Unstructured text comment to further describe the ExperimentStep.
        id (str): Anchor point for digital signature. This identifier is referred to \
            from the "Reference" element in a Signature. Unique per document.
        sourceDataLocation (str): Points to the original data source. May be a file name, uri, database ID, etc.
        templateUsed (str): Token with up to 1024 characters

    Children:
        tag_set (optional(TagSet)): Collection of Tags
        technique (optional(Technique)): Technique used
        infrastructure (optional(Infrastructure)): Infrastructure used
        method (optional(Method)): Method used in this step
        result (optional(list(Result))): Collection of Results
    """

    # Attributes
    experimentStepID: Annotated[str, ATTRIB] = field()
    name: Annotated[str, ATTRIB] = field()
    comment: Annotated[Optional[str], ATTRIB] = None
    id: Annotated[Optional[str], ATTRIB(regex=NC_NAME)] = None
    sourceDataLocation: Annotated[Optional[str], ATTRIB] = None
    templateUsed: Annotated[Optional[str], ATTRIB] = None

    # Children
    tag_set: Annotated[Optional[TagSet], CHILD] = None
    technique: Annotated[Optional[Technique], CHILD] = None
    infrastructure: Annotated[Optional[Infrastructure], CHILD] = None
    method: Annotated[Optional[Method], CHILD] = None
    result: Annotated[Optional[list[Result]], CHILD] = None


@dataclass
class ExperimentStepSet(XmlModel, regclass=AnIMLDocBase):
    """
    Container for multiple ExperimentSteps that describe the process and results.

    Children:
        templates (optional(list(Template))): Collection of Templates
        experiment_steps (list(ExperimentStep)): Collection of ExperimentSteps
    """

    # Children
    templates: Annotated[list[Template], CHILD] = field(default_factory=list)
    experiment_steps: Annotated[Optional[list[ExperimentStep]], CHILD] = field(
        default_factory=list
    )

    def append(self, item: ExperimentStep) -> ExperimentStep:
        """Add and return an ExperimentStep to the set"""
        self.experiment_steps.append(item)
        return item


@dataclass
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
    id: Annotated[Optional[str], ATTRIB(regex=NC_NAME)]
    name: Annotated[str, ATTRIB]

    # Children
    series: Annotated[Optional[SeriesSet], CHILD]
    category_set: Annotated[Optional[List[Category]], CHILD]
    experiment_step: Annotated[Optional[ExperimentStepSet], CHILD]


@dataclass
class Template(XmlModel, regclass=AnIMLDocBase):
    """
    Represents a template for an ExperimentStep.

    ```xml
    <Template templateID="..." name="..." id="..." sourceDataLocation="...">
        <TagSet .../>
        <Technique .../>
        <Infrastructure .../>
        <Method .../>
        <Result .../>
    </Template>
    ```

    Attributes:
        name (str): Name of the template
        templateID (str): Unique identifier for the template
        id (str): Anchor point for digital signature. This identifier is referred to \
            from the "Reference" element in a Signature. Unique per document.
        sourceDataLocation (str): Points to the original data source. May be a file \
            name, uri, database ID, etc.

        tag_set (TagSet | None): Set of Tag elements.
        technique (Technique | None): Reference to Technique Definition used in this Experiment.
        infrastructure (Infrastructure | None): Contains references to the context \
            of this Experiment.
        method (Method | None): Describes how this Experiment was performed.
        result (Result | None): Container for Data derived from Experiment.
    """

    name: Annotated[str, ATTRIB]
    templateID: Annotated[str, ATTRIB]
    id: Annotated[Optional[str], ATTRIB]
    sourceDataLocation: Annotated[Optional[str], ATTRIB]

    tag_set: Annotated[Optional[TagSet], CHILD] = None
    technique: Annotated[Optional[Technique], CHILD] = None
    infrastructure: Annotated[Optional[Infrastructure], CHILD] = None
    method: Annotated[Optional[Method], CHILD] = None
    result: Annotated[Optional[Result], CHILD] = None
