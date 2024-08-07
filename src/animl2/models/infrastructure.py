from dataclasses import dataclass
from enum import Enum
from typing import Annotated, Optional, Union, overload

from ..core import ATTRIB, CHILD, XmlModel
from ..utils.regex import NC_NAME
from .base import AnIMLDocBase
from .data_type import DoubleType, FloatType, IntType, LongType, Timestamp


class PurposeType(str, Enum):
    Produced = "produced"
    Consumed = "consumed"


AnIMLDocBase.register(PurposeType.__name__, PurposeType)


@dataclass
class ExperimentDataReference(XmlModel, regclass=AnIMLDocBase):
    """
    Reference to an Experiment Step whose data are consumed.

    ```xml
    <ExperimentDataReference
      dataPurpose="consumed"
      experimentStepID="..."
      role="..."
      id="..."
      />
    ```

    Attributes:
        dataPurpose (PurposeType): Specifies whether the referenced ExperimentStep \
            data is consumed or produced in an experiment.
        experimentStepID (str): Token with up to 1024 characters
        role (str): Token with up to 1024 characters
        id (str | None): Anchor point for digital signature. This identifier is referred \
            to from the "Reference" element in a Signature. Unique per document.
    """

    # Attributes
    dataPurpose: Annotated[PurposeType, ATTRIB]
    experimentStepID: Annotated[str, ATTRIB]
    role: Annotated[str, ATTRIB]
    id: Annotated[Optional[str], ATTRIB(regex=NC_NAME)] = None


@dataclass
class ExperimentDataBulkReference(XmlModel, regclass=AnIMLDocBase):
    """
    Prefix-based reference to a set of Experiment Steps whose data are consumed.

    ```xml
    <ExperimentDataBulkReference
      experimentStepIDPrefix="..."
      role="..."
      dataPurpose="consumed"
      id="..."
      />
    ```

    Attributes:
        dataPurpose (PurposeType): Specifies whether the referenced ExperimentStep \
            data is consumed or produced in an experiment.
        experimentStepIDPrefix (str): Token with up to 1024 characters
        id (str): Anchor point for digital signature. This identifier is referred \
            to from the "Reference" element in a Signature. Unique per document.
        role (str): Token with up to 1024 characters

    """

    # Attributes
    dataPurpose: Annotated[PurposeType, ATTRIB]
    experimentStepIDPrefix: Annotated[str, ATTRIB]
    role: Annotated[str, ATTRIB]
    id: Annotated[Optional[str], ATTRIB(regex=NC_NAME)] = None


@dataclass
class ExperimentDataReferenceSet(XmlModel, regclass=AnIMLDocBase):
    """
    Set of Experiment Steps consumed by this Experiment Step.

    ```xml
    <ExperimentDataReferenceSet id="...">
        <ExperimentDataReference .../>
        <ExperimentDataReference .../>
        <ExperimentDataBulkReference .../>
        <ExperimentDataBulkReference .../>
    </ExperimentDataReferenceSet>
    ```

    Attributes:
        id (str | None): Anchor point for digital signature. This identifier is referred \
            to from the "Reference" element in a Signature. Unique per document.
        experiment_reference_set (list[ExperimentDataReference] | None): Collection of ExperimentDataReferences
        experiment_bulk_reference_set (list[ExperimentDataBulkReference] | None): Collection of ExperimentDataBulkReferences
    """

    experiment_reference_set: Annotated[
        Optional[list[ExperimentDataReference]], CHILD
    ] = None
    experiment_bulk_reference_set: Annotated[
        Optional[list[ExperimentDataBulkReference]], CHILD
    ] = None

    id: Annotated[Optional[str], ATTRIB(regex=NC_NAME)] = None

    @overload
    def append(self, item: ExperimentDataReference) -> ExperimentDataReference:
        """Add an ExperimentDataReference to the set"""

    @overload
    def append(self, item: ExperimentDataBulkReference) -> ExperimentDataBulkReference:
        """Add an ExperimentDataBulkReference to the set"""

    def append(self, item):
        if isinstance(item, ExperimentDataReference):
            if self.experiment_reference_set is None:
                self.experiment_reference_set = list()
            self.experiment_reference_set.append(item)
        elif isinstance(item, ExperimentDataBulkReference):
            if self.experiment_bulk_reference_set is None:
                self.experiment_bulk_reference_set = list()
            self.experiment_bulk_reference_set.append(item)
        return item


@dataclass
class StartValue(XmlModel, regclass=AnIMLDocBase):
    """
    Lower boundary of an interval or ValueSet.

    ```xml
    <StartValue>
        <Double>...</Double> or <Float>...</Float> or <Int>...</Int> or <Long>...</Long>
    </StartValue>
    ```

    Attributes:
        value (Union[DoubleType, FloatType, IntType, LongType]): Value of the StartValue.

    """

    # Children
    value: Annotated[Union[DoubleType, FloatType, IntType, LongType], CHILD]


@dataclass
class EndValue(XmlModel, regclass=AnIMLDocBase):
    """
    Upper boundary of an interval or ValueSet.

    ```xml
    <EndValue>
        <Double>...</Double> or <Float>...</Float> or <Int>...</Int> or <Long>...</Long>
    </EndValue>
    ```

    Attributes:
        value (Union[DoubleType, FloatType, IntType, LongType]): Value of the EndValue.

    """

    # Children
    value: Annotated[Union[DoubleType, FloatType, IntType, LongType], CHILD]


@dataclass
class Increment(XmlModel, regclass=AnIMLDocBase):
    """
    Increment value

    ```xml
    <Increment>
        <Double>...</Double> or <Float>...</Float> or <Int>...</Int> or <Long>...</Long>
    </Increment>
    ```

    Attributes:
        value (Union[DoubleType, FloatType, IntType, LongType]): Value of the Increment.
    """

    # Children
    value: Annotated[Union[DoubleType, FloatType, IntType, LongType], CHILD]


@dataclass
class ParentDataPointReference(XmlModel, regclass=AnIMLDocBase):
    """
    Reference to a data point or value range in an independent Series in the parent Result.

    ```xml
    <ParentDataPointReference id="..." seriesID="...">
        <StartValue>...</StartValue>
        <EndValue>...</EndValue>
    </ParentDataPointReference>
    ```

    Attributes:
        id (str): Anchor point for digital signature. This identifier is \
            referred to from the "Reference" element in a Signature. Unique per document.
        seriesID (str): Contains the ID of the Series referenced.
        start_value (StartValue): Lower boundary
        end_value (EndValue): Upper boundary
    """

    # Attributes
    id: Annotated[Optional[str], ATTRIB(regex=NC_NAME)]
    seriesID: Annotated[str, ATTRIB]

    # Children
    start_value: Annotated[StartValue, CHILD]
    end_value: Annotated[EndValue, CHILD]


@dataclass
class ParentDataPointReferenceSet(XmlModel, regclass=AnIMLDocBase):
    """
    Contains references to the parent Result.

    ```xml
    <ParentDataPointReferenceSet>
        <ParentDataPointReference .../>
        <ParentDataPointReference .../>
    </ParentDataPointReferenceSet>
    ```

    Attributes:
        data_point_reference_set (list[DataPointReference]): Collection of DataPointReferences
    """

    # Children
    data_point_reference_set: Annotated[
        Optional[list[ParentDataPointReference]], CHILD
    ] = None

    @overload
    def append(self, item: ParentDataPointReference) -> ParentDataPointReference:
        """Add a DataPointReference to the set"""

    def append(self, item):
        if self.data_point_reference_set is None:
            self.data_point_reference_set = list()
        self.data_point_reference_set.append(item)
        return item


@dataclass
class SampleReference(XmlModel, regclass=AnIMLDocBase):
    """
    Reference to a Sample used in this Experiment.

    ```xml
    <SampleReference
      id="..."
      role="..."
      sampleID="..."
      samplePurpose="..."
      />
    ```

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
    role: Annotated[str, ATTRIB]
    sampleID: Annotated[str, ATTRIB]
    samplePurpose: Annotated[PurposeType, ATTRIB]
    id: Annotated[Optional[str], ATTRIB(regex=NC_NAME)] = None


@dataclass
class SampleInheritance(XmlModel, regclass=AnIMLDocBase):
    """
    Indicates that a Sample was inherited from the parent ExperimentStep.

    ```xml
    <SampleInheritance
      id="..."
      role="..."
      samplePurpose="..."
      />
    ```

    Attributes:
        id (str): Anchor point for digital signature. This identifier is \
            referred to from the "Reference" element in a Signature. Unique per document.
        role (str): Role this sample plays within the current ExperimentStep.
        samplePurpose (PurposeTypes): Specifies whether the referenced sample \
            is produced or consumed by the current ExperimentStep.
    """

    # Attributes
    role: Annotated[str, ATTRIB]
    samplePurpose: Annotated[PurposeType, ATTRIB]
    id: Annotated[Optional[str], ATTRIB(regex=NC_NAME)] = None


@dataclass
class SampleReferenceSet(XmlModel, regclass=AnIMLDocBase):
    """
    Set of Samples used in this Experiment.

    ```xml
    <SampleReferenceSet id="...">
        <SampleReference .../>
        <SampleReference .../>
        <SampleInheritance .../>
        <SampleInheritance .../>
    </SampleReferenceSet>
    ```

    Attributes:
        id (str): Anchor point for digital signature. This identifier is \
            referred to from the "Reference" element in a Signature. Unique per document.
        sample_references (list[SampleReference]): Collection of SampleReferences
        sample_inheritances (list[SampleInheritance]): Collection of SampleInheritances
    """

    # Attributes
    id: Annotated[Optional[str], ATTRIB(regex=NC_NAME)] = None

    # Children
    sample_references: Annotated[Optional[list[SampleReference]], CHILD] = None
    sample_inheritances: Annotated[Optional[list[SampleInheritance]], CHILD] = None

    @overload
    def append(self, item: SampleReference) -> SampleReference:
        """Add a SampleReference to the set"""

    @overload
    def append(self, item: SampleInheritance) -> SampleInheritance:
        """Add a SampleInheritance to the set"""

    def append(self, item):
        if isinstance(item, SampleReference):
            if self.sample_references is None:
                self.sample_references = list()
            self.sample_references.append(item)
        elif isinstance(item, SampleInheritance):
            if self.sample_inheritances is None:
                self.sample_inheritances = list()
            self.sample_inheritances.append(item)
        return item


@dataclass
class Infrastructure(XmlModel, regclass=AnIMLDocBase):
    """
    Contains references to the context of this Experiment.

    ```xml
    <Infrastructure id="...">
        <SampleReferenceSet .../>
        <ParentDataPointReferenceSet .../>
        <ExperimentDataReferenceSet .../>
        <DateTime>...</DateTime>
    </Infrastructure>
    ```

    Attributes:
        id (str | None): Anchor point for digital signature. This identifier is \
            referred to from the "Reference" element in a Signature. Unique per document.
        sample_reference_set (SampleReferenceSet | None): Collection of SampleReferences
        parent_datapoint_refence_set (DataPointReferenceSet | None): Collection of DataPointReferences
        experiment_data_reference_set (ExperimentDataReferenceSet | None): Collection of ExperimentDataReferences
        time_stamp (Timestamp | None): Time stamp of the Infrastructure.

    """

    # Attributes
    id: Annotated[Optional[str], ATTRIB(regex=NC_NAME)] = None

    # Children
    sample_reference_set: Annotated[Optional[SampleReferenceSet], CHILD] = None
    parent_datapoint_refence_set: Annotated[
        Optional[ParentDataPointReferenceSet], CHILD
    ] = None
    experiment_data_reference_set: Annotated[
        Optional[ExperimentDataReferenceSet], CHILD
    ] = None
    time_stamp: Annotated[Optional[Timestamp], CHILD] = None

    @overload
    def append(self, item: SampleReference) -> SampleReference:
        """Add a SampleReference to the Infrastructure"""

    @overload
    def append(self, item: SampleInheritance) -> SampleInheritance:
        """Add a SampleInheritance to the Infrastructure"""

    @overload
    def append(self, item: ParentDataPointReference) -> ParentDataPointReference:
        """Add a DataPointReference to the Infrastructure"""

    @overload
    def append(self, item: ExperimentDataReference) -> ExperimentDataReference:
        """Add an ExperimentDataReference to the Infrastructure"""

    @overload
    def append(self, item: ExperimentDataBulkReference) -> ExperimentDataBulkReference:
        """Add an ExperimentDataBulkReference to the Infrastructure"""

    def append(self, item):
        if isinstance(item, SampleReference):
            if self.sample_reference_set is None:
                self.sample_reference_set = SampleReferenceSet()
            self.sample_reference_set.append(item)
        elif isinstance(item, SampleInheritance):
            if self.sample_reference_set is None:
                self.sample_reference_set = SampleReferenceSet()
            self.sample_reference_set.append(item)
        elif isinstance(item, ParentDataPointReference):
            if self.parent_datapoint_refence_set is None:
                self.parent_datapoint_refence_set = ParentDataPointReferenceSet()
            self.parent_datapoint_refence_set.append(item)
        elif isinstance(item, ExperimentDataReference):
            if self.experiment_data_reference_set is None:
                self.experiment_data_reference_set = ExperimentDataReferenceSet()
            self.experiment_data_reference_set.append(item)
        elif isinstance(item, ExperimentDataBulkReference):
            if self.experiment_data_reference_set is None:
                self.experiment_data_reference_set = ExperimentDataReferenceSet()
            self.experiment_data_reference_set.append(item)
        else:
            raise ValueError(f"Cannot append {item} to Infrastructure")
        return item
