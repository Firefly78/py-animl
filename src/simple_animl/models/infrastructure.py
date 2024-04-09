from datetime import datetime
from enum import Enum
from typing import Optional, Union

from ..core import Field, XmlModel
from ..utils.regex import NC_NAME
from .base import AnIMLDocBase
from .data_type import DateTimeType, DoubleType, FloatType, IntType, LongType


class PurposeType(str, Enum):
    Produced = "produced"
    Consumed = "consumed"


AnIMLDocBase.register(PurposeType.__name__, PurposeType)


class ExperimentDataReference(XmlModel, regclass=AnIMLDocBase):
    """
    Reference to an Experiment Step whose data are consumed.

    Attributes:
        dataPurpose (PurposeType): Specifies whether the referenced ExperimentStep \
            data is consumed or produced in an experiment.
        experimentStepID (str): Token with up to 1024 characters
        id (str): Anchor point for digital signature. This identifier is referred \
            to from the "Reference" element in a Signature. Unique per document.
        role (str): Token with up to 1024 characters
    """

    # Attributes
    dataPurpose: PurposeType = Field.Attribute()
    experimentStepID: str = Field.Attribute()
    id: Optional[str] = Field.Attribute(regex=NC_NAME)
    role: str = Field.Attribute()


class ExperimentDataBulkReference(XmlModel, regclass=AnIMLDocBase):
    """
    Prefix-based reference to a set of Experiment Steps whose data are consumed.

    Attributes:
        dataPurpose (PurposeType): Specifies whether the referenced ExperimentStep \
            data is consumed or produced in an experiment.
        experimentStepIDPrefix (str): Token with up to 1024 characters
        id (str): Anchor point for digital signature. This identifier is referred \
            to from the "Reference" element in a Signature. Unique per document.
        role (str): Token with up to 1024 characters

    """

    # Attributes
    dataPurpose: PurposeType = Field.Attribute()
    experimentStepIDPrefix: str = Field.Attribute()
    id: Optional[str] = Field.Attribute(regex=NC_NAME)
    role: str = Field.Attribute()


class ExperimentDataReferenceSet(XmlModel, regclass=AnIMLDocBase):
    """
    Set of Experiment Steps consumed by this Experiment Step.

    Attributes:
        id (str): Anchor point for digital signature. This identifier is referred \
            to from the "Reference" element in a Signature. Unique per document.

    Children:
        experiment_reference_set (list(ExperimentDataReference)): Collection of ExperimentDataReferences
        experiment_bulk_reference_set (list(ExperimentDataBulkReference)): Collection of ExperimentDataBulkReferences
    """

    id: Optional[str] = Field.Attribute(regex=NC_NAME)

    experiment_reference_set: list[ExperimentDataReference] = Field.Child()
    experiment_bulk_reference_set: list[ExperimentDataBulkReference] = Field.Child()


class StartValue(XmlModel, regclass=AnIMLDocBase):
    """
    Lower boundary of an interval or ValueSet.

    Children:
        value (Union[DoubleType, FloatType, IntType, LongType]): Value of the StartValue.

    """

    # Children
    value: Union[DoubleType, FloatType, IntType, LongType] = Field.Child()


class EndValue(XmlModel, regclass=AnIMLDocBase):
    """
    Upper boundary of an interval or ValueSet.

    Children:
        value (Union[DoubleType, FloatType, IntType, LongType]): Value of the EndValue.

    """

    # Children
    value: Union[DoubleType, FloatType, IntType, LongType] = Field.Child()


class ParentDataPointReference(XmlModel, regclass=AnIMLDocBase):
    """
    Reference to a data point or value range in an independent Series in the parent Result.

    Attributes:
        id (str): Anchor point for digital signature. This identifier is \
            referred to from the "Reference" element in a Signature. Unique per document.
        seriesID (str): Contains the ID of the Series referenced.

    Children:
        start_value (StartValue): Lower boundary
        end_value (EndValue): Upper boundary
    """

    # Attributes
    id: Optional[str] = Field.Attribute(regex=NC_NAME)
    seriesID: str = Field.Attribute()

    # Children
    start_value: StartValue = Field.Child()
    end_value: EndValue = Field.Child()


class ParentDataPointReferenceSet(XmlModel, regclass=AnIMLDocBase):
    """
    Contains references to the parent Result.

    Children:
        data_point_reference_set (list(DataPointReference)): Collection of DataPointReferences
    """

    # Children
    data_point_reference_set: list[ParentDataPointReference] = Field.Child()


class SampleReference(XmlModel, regclass=AnIMLDocBase):
    """
    Reference to a Sample used in this Experiment.

    Attributes:
        id (str): Anchor point for digital signature. This identifier is \
            referred to from the "Reference" element in a Signature. Unique per document.
        role (str): Role this sample plays within the current ExperimentStep.
        sampleID (str): SampleID of the Sample used in the current ExperimentStep. \
            Refers to the sampleID within the SampleSet section of the document.
        samplePurpose (PurposeTypes): Specifies whether the referenced sample \
            is produced or consumed by the current ExperimentStep.
    """

    # Attributes
    id: Optional[str] = Field.Attribute(regex=NC_NAME)
    role: str = Field.Attribute()
    sampleID: str = Field.Attribute()
    samplePurpose: PurposeType = Field.Attribute()


class SampleInheritance(XmlModel, regclass=AnIMLDocBase):
    """
    Indicates that a Sample was inherited from the parent ExperimentStep.

    Attributes:
        id (str): Anchor point for digital signature. This identifier is \
            referred to from the "Reference" element in a Signature. Unique per document.
        role (str): Role this sample plays within the current ExperimentStep.
        samplePurpose (PurposeTypes): Specifies whether the referenced sample \
            is produced or consumed by the current ExperimentStep.
    """

    # Attributes
    id: Optional[str] = Field.Attribute(regex=NC_NAME)
    role: str = Field.Attribute()
    samplePurpose: PurposeType = Field.Attribute()


class SampleReferenceSet(XmlModel, regclass=AnIMLDocBase):
    """
    Set of Samples used in this Experiment.

    Attributes:
        id (str): Anchor point for digital signature. This identifier is \
            referred to from the "Reference" element in a Signature. Unique per document.

    Children:
        sample_references (list(SampleReference)): Collection of SampleReferences
        sample_inheritances (list(SampleInheritance)): Collection of SampleInheritances
    """

    # Attributes
    id: Optional[str] = Field.Attribute(regex=NC_NAME)

    # Children
    sample_references: list[SampleReference] = Field.Child()
    sample_inheritances: list[SampleInheritance] = Field.Child()


class Infrastructure(XmlModel, regclass=AnIMLDocBase):
    """
    Contains references to the context of this Experiment.

    Attributes:
        id (str): Anchor point for digital signature. This identifier is \
            referred to from the "Reference" element in a Signature. Unique per document.

    Children:
        sample_reference_set (SampleReferenceSet): Collection of SampleReferences
        parent_datapoint_refence_set (DataPointReferenceSet): Collection of DataPointReferences
        experiment_data_reference_set (ExperimentDataReferenceSet): Collection of ExperimentDataReferences
        time_stamp (DateTimeType): Time stamp of the Infrastructure.

    """

    # Attributes
    id: Optional[str] = Field.Attribute(regex=NC_NAME)

    # Children
    sample_reference_set: Optional[SampleReferenceSet] = Field.Child()
    parent_datapoint_refence_set: Optional[ParentDataPointReferenceSet] = Field.Child()
    experiment_data_reference_set: Optional[ExperimentDataReferenceSet] = Field.Child()
    time_stamp: Optional[DateTimeType] = Field.Child()
