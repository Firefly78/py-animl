from __future__ import annotations

from dataclasses import dataclass
from io import StringIO, TextIOWrapper
from typing import IO, Annotated, Optional, Union, overload
from xml.etree.ElementTree import ElementTree

from ..core import ATTRIB, CHILD, XmlModel, scrub_namespace
from .base import AnIMLDocBase
from .experiment import ExperimentStep, ExperimentStepSet
from .sample import Sample, SampleSet

VERSION: str = "0.90"
XMLNS: str = "urn:org:astm:animl:schema:core:draft:0.90"
XMLNS_XSI: str = "http://www.w3.org/2001/XMLSchema-instance"
XSI_SCHEMALOCATION: str = XMLNS + " http://schemas.animl.org/current/animl-core.xsd"


@dataclass
class AnIMLDoc(XmlModel, regclass=AnIMLDocBase):
    """
    Root Element for AnIML documents.

    ```xml
    <AnIML ...>
        <SampleSet>...</SampleSet>
        <ExperimentStepSet>...</ExperimentStepSet>
        <!-- Audit Trail -->
        <!-- Signatures -->
    </AnIML>
    ```

    Attributes:
        version (str): Version of AnIML
        xmlns (str): XML namespace
        xmlns_xsi (str): XML namespace for schema instance
        xsi_schemalocation (str): Schema location
        sample_set (SampleSet | None): Collection of Samples
        experiment_set (ExperimentStepSet | None): Collection of Experiment Steps


    """

    tag = "AnIML"  # Override name to use during serialization

    # Manadatory attributes
    version: Annotated[Optional[str], ATTRIB] = VERSION
    xmlns: Annotated[Optional[str], ATTRIB] = XMLNS
    xmlns_xsi: Annotated[Optional[str], ATTRIB(alias="xmlns:xsi")] = XMLNS_XSI
    xsi_schemalocation: Annotated[Optional[str], ATTRIB(alias="xsi:schemaLocation")] = (
        XSI_SCHEMALOCATION
    )

    # Children
    sample_set: Annotated[Optional[SampleSet], CHILD] = None
    experiment_set: Annotated[Optional[ExperimentStepSet], CHILD] = None
    # audit_trail_entry_set: Annotated[Optional[AuditTrailEntrySet], CHILD]
    # signature_set: Annotated[Optional[SignatureSet], CHILD]

    @classmethod
    def loads(cls, xml: Union[IO, str]) -> AnIMLDoc:
        if isinstance(xml, str):
            xml = StringIO(xml)
        elif isinstance(xml, (TextIOWrapper,)):
            pass  # Nothing
        else:
            raise TypeError(f"Expected str or IO, got {type(xml)}")
        et = ElementTree()
        et.parse(source=xml)
        scrub_namespace(et.getroot())
        return cls.load_xml(et.getroot())

    @overload
    def append(self, item: ExperimentStep) -> ExperimentStep:
        """Add an experiment step to the document"""

    @overload
    def append(self, item: Sample) -> Sample:
        """Add a sample to the document"""

    def append(self, item):
        if isinstance(item, ExperimentStep):
            if self.experiment_set is None:
                self.experiment_set = ExperimentStepSet()
            return self.experiment_set.append(item)
        elif isinstance(item, Sample):
            if self.sample_set is None:
                self.sample_set = SampleSet()
            return self.sample_set.append(item)
        else:
            raise TypeError(f"Expected Sample or ExperimentStep, got {type(item)}")


def create_document():
    """Creates a new AnIML document"""
    return AnIMLDoc()


def open_document(xml: Union[IO, str]):
    """Opens an existing AnIML document"""
    return AnIMLDoc.loads(xml)
