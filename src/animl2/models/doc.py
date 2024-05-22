from __future__ import annotations

from dataclasses import dataclass
from io import StringIO
from typing import IO, Annotated, Optional, Union
from xml.etree.ElementTree import ElementTree

from ..core import ATTRIB, CHILD, XmlModel, scrub_namespace
from .base import AnIMLDocBase
from .experiment import ExperimentStep, ExperimentStepSet
from .sample import Sample, SampleSet

VERSION: str = "0.90"
XMLNS: str = "urn:org:astm:animl:schema:core:draft:0.90"
XMLNS_XSI: str = "http://www.w3.org/2001/XMLSchema-instance"
XSI_SCHEMALOCATION: str = (
    "urn:org:astm:animl:schema:core:draft:0.90 http://schemas.animl.org/current/animl-core.xsd"
)


@dataclass
class AnIMLDoc(XmlModel, regclass=AnIMLDocBase):
    """
    Root Element for AnIML documents.

    Attributes:
        version (str): Version of AnIML
        xmlns (str): XML namespace
        xmlns_xsi (str): XML namespace for schema instance
        xsi_schemalocation (str): Schema location

    Children:
        sample_set (optional(SampleSet)): Collection of Samples
        experiment_set (optional(ExperimentStepSet)): Collection of Experiment Steps
        TODO: Add more children

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
    # audit_trail_entry_set: Optional[AuditTrailEntrySet] = CHILD()
    # signature_set: Optional[SignatureSet] = CHILD()

    @classmethod
    def loads(cls, xml: Union[IO, str]) -> AnIMLDoc:
        if isinstance(xml, str):
            xml = StringIO(xml)
        elif isinstance(xml, IO):
            pass  # Nothing
        else:
            raise TypeError(f"Expected str or IO, got {type(xml)}")
        et = ElementTree()
        et.parse(source=xml)
        scrub_namespace(et.getroot())
        return cls.load_xml(et.getroot())

    def append(self, item: Union[ExperimentStep, Sample]):
        """Add and return a sample to the document"""
        if isinstance(item, ExperimentStep):
            if self.experiment_set is None:
                self.experiment_set = ExperimentStepSet()
            self.experiment_set.append(item)
        elif isinstance(item, Sample):
            if self.sample_set is None:
                self.sample_set = SampleSet()
            return self.sample_set.append(item)


def create_document():
    """Creates a new AnIML document"""
    return AnIMLDoc()


def open_document(xml: Union[IO, str]):
    """Opens an existing AnIML document"""
    return AnIMLDoc.loads(xml)
