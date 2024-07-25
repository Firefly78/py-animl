import datetime
import unittest

from helpers import make_element

from animl2.core import XmlModel
from animl2.models.data_type import IntType, Timestamp
from animl2.models.infrastructure import (
    EndValue,
    ExperimentDataBulkReference,
    ExperimentDataReference,
    ExperimentDataReferenceSet,
    Increment,
    Infrastructure,
    ParentDataPointReference,
    ParentDataPointReferenceSet,
    SampleInheritance,
    SampleReference,
    SampleReferenceSet,
    StartValue,
)


class Test_ExperimentDataReference(unittest.TestCase):
    def test_Inheritance(self):
        self.assertTrue(issubclass(ExperimentDataReference, XmlModel))

    def test_Dump(self):
        obj = ExperimentDataReference(
            dataPurpose="consumed",
            experimentStepID="c1234",
            role="input",
            id="c1",
        )
        xml = obj.dump_xml()

        self.assertIsNotNone(xml)
        self.assertEqual(xml.tag, "ExperimentDataReference")

        self.assertEqual(xml.attrib["dataPurpose"], "consumed")
        self.assertEqual(xml.attrib["experimentStepID"], "c1234")
        self.assertEqual(xml.attrib["role"], "input")
        self.assertEqual(xml.attrib["id"], "c1")

    def test_Load(self):
        xml = make_element(
            "ExperimentDataReference",
            attrib={
                "dataPurpose": "consumed",
                "experimentStepID": "c1234",
                "role": "input",
                "id": "c1",
            },
        )

        obj = ExperimentDataReference.load_xml(xml)
        self.assertIsInstance(obj, ExperimentDataReference)
        self.assertEqual(obj.dataPurpose, "consumed")
        self.assertEqual(obj.experimentStepID, "c1234")
        self.assertEqual(obj.role, "input")
        self.assertEqual(obj.id, "c1")


class Test_ExperimentDataBulkReference(unittest.TestCase):
    def test_Inheritance(self):
        self.assertTrue(issubclass(ExperimentDataBulkReference, XmlModel))

    def test_Dump(self):
        obj = ExperimentDataBulkReference(
            id="c1",
            dataPurpose="consumed",
            experimentStepIDPrefix="c",
            role="input",
        )
        xml = obj.dump_xml()

        self.assertIsNotNone(xml)
        self.assertEqual(xml.tag, "ExperimentDataBulkReference")

        self.assertEqual(xml.attrib["dataPurpose"], "consumed")
        self.assertEqual(xml.attrib["experimentStepIDPrefix"], "c")
        self.assertEqual(xml.attrib["role"], "input")
        self.assertEqual(xml.attrib["id"], "c1")

    def test_Load(self):
        xml = make_element(
            "ExperimentDataBulkReference",
            attrib={
                "dataPurpose": "consumed",
                "experimentStepIDPrefix": "c1234",
                "role": "input",
                "id": "c1",
            },
        )

        obj = ExperimentDataBulkReference.load_xml(xml)
        self.assertIsInstance(obj, ExperimentDataBulkReference)
        self.assertEqual(obj.dataPurpose, "consumed")
        self.assertEqual(obj.experimentStepIDPrefix, "c1234")
        self.assertEqual(obj.role, "input")
        self.assertEqual(obj.id, "c1")


class Test_ExperimentDataReferenceSet(unittest.TestCase):
    def test_Inheritance(self):
        self.assertTrue(issubclass(ExperimentDataReferenceSet, XmlModel))

    def test_Dump(self):
        obj = ExperimentDataReferenceSet(
            experiment_reference_set=[
                ExperimentDataReference(
                    dataPurpose="consumed",
                    experimentStepID="c1234",
                    role="input",
                    id="c1",
                )
            ],
            experiment_bulk_reference_set=[
                ExperimentDataBulkReference(
                    id="c1",
                    dataPurpose="consumed",
                    experimentStepIDPrefix="c",
                    role="input",
                )
            ],
        )
        xml = obj.dump_xml()

        self.assertIsNotNone(xml)
        self.assertEqual(xml.tag, "ExperimentDataReferenceSet")

        self.assertEqual(len(xml.findall("ExperimentDataReference")), 1)
        self.assertEqual(len(xml.findall("ExperimentDataBulkReference")), 1)

    def test_Load(self):
        xml = make_element(
            "ExperimentDataReferenceSet",
            children=[
                make_element(
                    "ExperimentDataReference",
                    attrib={
                        "dataPurpose": "consumed",
                        "experimentStepID": "c1234",
                        "role": "input",
                        "id": "c1",
                    },
                ),
                make_element(
                    "ExperimentDataBulkReference",
                    attrib={
                        "dataPurpose": "consumed",
                        "experimentStepIDPrefix": "c1234",
                        "role": "input",
                        "id": "c1",
                    },
                ),
            ],
        )

        obj = ExperimentDataReferenceSet.load_xml(xml)
        self.assertIsInstance(obj, ExperimentDataReferenceSet)
        self.assertIsInstance(obj.experiment_reference_set[0], ExperimentDataReference)
        self.assertIsInstance(
            obj.experiment_bulk_reference_set[0], ExperimentDataBulkReference
        )


class Test_StartValue(unittest.TestCase):
    def test_Inheritance(self):
        self.assertTrue(issubclass(StartValue, XmlModel))

    def test_Dump(self):
        obj = StartValue(value=IntType(1))
        xml = obj.dump_xml()

        self.assertIsNotNone(xml)
        self.assertEqual(xml.tag, "StartValue")
        self.assertEqual(xml.find("I").text, "1")

    def test_Load(self):
        xml = make_element(
            "StartValue",
            children=[
                make_element("I", text="1"),
            ],
        )

        obj = StartValue.load_xml(xml)
        self.assertIsInstance(obj, StartValue)
        self.assertEqual(obj.value.value, 1)


class Test_EndValue(unittest.TestCase):
    def test_Inheritance(self):
        self.assertTrue(issubclass(EndValue, XmlModel))

    def test_Dump(self):
        obj = EndValue(value=IntType(1))
        xml = obj.dump_xml()

        self.assertIsNotNone(xml)
        self.assertEqual(xml.tag, "EndValue")
        self.assertEqual(xml.find("I").text, "1")

    def test_Load(self):
        xml = make_element(
            "EndValue",
            children=[
                make_element("I", text="1"),
            ],
        )

        obj = EndValue.load_xml(xml)
        self.assertIsInstance(obj, EndValue)
        self.assertEqual(obj.value.value, 1)


class Test_Increment(unittest.TestCase):
    def test_Inheritance(self):
        self.assertTrue(issubclass(Increment, XmlModel))

    def test_Dump(self):
        obj = Increment(value=IntType(1))
        xml = obj.dump_xml()

        self.assertIsNotNone(xml)
        self.assertEqual(xml.tag, "Increment")
        self.assertEqual(xml.find("I").text, "1")

    def test_Load(self):
        xml = make_element(
            "Increment",
            children=[
                make_element("I", text="1"),
            ],
        )

        obj = Increment.load_xml(xml)
        self.assertIsInstance(obj, Increment)
        self.assertEqual(obj.value.value, 1)


class Test_ParentDataPointReference(unittest.TestCase):
    def test_Inheritance(self):
        self.assertTrue(issubclass(ParentDataPointReference, XmlModel))

    def test_Dump(self):
        obj = ParentDataPointReference(
            id="c1",
            seriesID="c2",
            start_value=StartValue(value=IntType(1)),
            end_value=EndValue(value=IntType(2)),
        )
        xml = obj.dump_xml()

        self.assertIsNotNone(xml)
        self.assertEqual(xml.tag, "ParentDataPointReference")

        self.assertEqual(xml.attrib["id"], "c1")
        self.assertEqual(xml.attrib["seriesID"], "c2")
        self.assertEqual(xml.find("StartValue").find("I").text, "1")
        self.assertEqual(xml.find("EndValue").find("I").text, "2")

    def test_Load(self):
        xml = make_element(
            "ParentDataPointReference",
            attrib={"id": "c1", "seriesID": "c2"},
            children=[
                make_element(
                    "StartValue",
                    children=[
                        make_element("I", text="1"),
                    ],
                ),
                make_element(
                    "EndValue",
                    children=[
                        make_element("I", text="2"),
                    ],
                ),
            ],
        )

        obj = ParentDataPointReference.load_xml(xml)
        self.assertIsInstance(obj, ParentDataPointReference)
        self.assertEqual(obj.id, "c1")
        self.assertEqual(obj.seriesID, "c2")
        self.assertEqual(obj.start_value.value.value, 1)
        self.assertEqual(obj.end_value.value.value, 2)


class Test_ParentDataPointReferenceSet(unittest.TestCase):
    def test_Inheritance(self):
        self.assertTrue(issubclass(ParentDataPointReferenceSet, XmlModel))

    def test_Dump(self):
        obj = ParentDataPointReferenceSet(
            data_point_reference_set=[
                ParentDataPointReference(
                    id="c1",
                    seriesID="c2",
                    start_value=StartValue(value=IntType(1)),
                    end_value=EndValue(value=IntType(2)),
                )
            ]
        )
        xml = obj.dump_xml()

        self.assertIsNotNone(xml)
        self.assertEqual(xml.tag, "ParentDataPointReferenceSet")

        self.assertEqual(len(xml.findall("ParentDataPointReference")), 1)

    def test_Load(self):
        xml = make_element(
            "ParentDataPointReferenceSet",
            children=[
                make_element(
                    "ParentDataPointReference",
                    attrib={"id": "c1", "seriesID": "c2"},
                    children=[
                        make_element(
                            "StartValue",
                            children=[
                                make_element("I", text="1"),
                            ],
                        ),
                        make_element(
                            "EndValue",
                            children=[
                                make_element("I", text="2"),
                            ],
                        ),
                    ],
                ),
            ],
        )

        obj = ParentDataPointReferenceSet.load_xml(xml)
        self.assertIsInstance(obj, ParentDataPointReferenceSet)
        self.assertIsInstance(obj.data_point_reference_set[0], ParentDataPointReference)


class Test_SampleReference(unittest.TestCase):
    def test_Inheritance(self):
        self.assertTrue(issubclass(SampleReference, XmlModel))

    def test_Dump(self):
        obj = SampleReference(
            id="c1", role="input", sampleID="c2", samplePurpose="consumed"
        )
        xml = obj.dump_xml()

        self.assertIsNotNone(xml)
        self.assertEqual(xml.tag, "SampleReference")

        self.assertEqual(xml.attrib["id"], "c1")
        self.assertEqual(xml.attrib["role"], "input")
        self.assertEqual(xml.attrib["sampleID"], "c2")
        self.assertEqual(xml.attrib["samplePurpose"], "consumed")

    def test_Load(self):
        xml = make_element(
            "SampleReference",
            attrib={
                "id": "c1",
                "role": "input",
                "sampleID": "c2",
                "samplePurpose": "consumed",
            },
        )

        obj = SampleReference.load_xml(xml)
        self.assertIsInstance(obj, SampleReference)
        self.assertEqual(obj.id, "c1")
        self.assertEqual(obj.role, "input")
        self.assertEqual(obj.sampleID, "c2")
        self.assertEqual(obj.samplePurpose, "consumed")


class Test_SampleInheritance(unittest.TestCase):
    def test_Inheritance(self):
        self.assertTrue(issubclass(SampleInheritance, XmlModel))

    def test_Dump(self):
        obj = SampleInheritance(id="c1", role="role", samplePurpose="consumed")
        xml = obj.dump_xml()

        self.assertIsNotNone(xml)
        self.assertEqual(xml.tag, "SampleInheritance")

        self.assertEqual(xml.attrib["id"], "c1")
        self.assertEqual(xml.attrib["role"], "role")
        self.assertEqual(xml.attrib["samplePurpose"], "consumed")

    def test_Load(self):
        xml = make_element(
            "SampleInheritance",
            attrib={"id": "c1", "role": "role", "samplePurpose": "consumed"},
        )

        obj = SampleInheritance.load_xml(xml)
        self.assertIsInstance(obj, SampleInheritance)
        self.assertEqual(obj.id, "c1")
        self.assertEqual(obj.role, "role")
        self.assertEqual(obj.samplePurpose, "consumed")


class Test_SampleReferenceSet(unittest.TestCase):
    def test_Inheritance(self):
        self.assertTrue(issubclass(SampleReferenceSet, XmlModel))

    def test_Dump(self):
        obj = SampleReferenceSet(
            sample_references=[
                SampleReference(
                    id="c1",
                    role="input",
                    sampleID="c2",
                    samplePurpose="consumed",
                )
            ],
            sample_inheritances=[
                SampleInheritance(id="c1", role="role", samplePurpose="consumed"),
            ],
        )
        xml = obj.dump_xml()

        self.assertIsNotNone(xml)
        self.assertEqual(xml.tag, "SampleReferenceSet")

        self.assertEqual(len(xml.findall("SampleReference")), 1)
        self.assertEqual(len(xml.findall("SampleInheritance")), 1)

    def test_Load(self):
        xml = make_element(
            "SampleReferenceSet",
            children=[
                make_element(
                    "SampleReference",
                    attrib={
                        "id": "c1",
                        "role": "input",
                        "sampleID": "c2",
                        "samplePurpose": "consumed",
                    },
                ),
                make_element(
                    "SampleInheritance",
                    attrib={"id": "c1", "role": "role", "samplePurpose": "consumed"},
                ),
            ],
        )

        obj = SampleReferenceSet.load_xml(xml)
        self.assertIsInstance(obj, SampleReferenceSet)
        self.assertIsInstance(obj.sample_references[0], SampleReference)
        self.assertIsInstance(obj.sample_inheritances[0], SampleInheritance)


class Test_Infrastructure(unittest.TestCase):
    def test_Inheritance(self):
        self.assertTrue(issubclass(Infrastructure, XmlModel))

    def test_Dump(self):
        obj = Infrastructure(id="c1")
        obj.time_stamp = Timestamp(datetime.datetime(2021, 1, 1, 0, 0, 0))
        obj.append(
            ExperimentDataReference(
                dataPurpose="consumed",
                experimentStepID="c1234",
                role="input",
                id="c1",
            )
        )
        xml = obj.dump_xml()

        self.assertIsNotNone(xml)
        self.assertEqual(xml.tag, "Infrastructure")

        self.assertEqual(xml.attrib["id"], "c1")

        self.assertEqual(len(xml.findall("ExperimentDataReferenceSet")), 1)

    def test_Load(self):
        xml = make_element(
            "Infrastructure",
            attrib={"id": "c1"},
            children=[
                make_element(
                    "ExperimentDataReferenceSet",
                    children=[
                        make_element(
                            "ExperimentDataReference",
                            attrib={
                                "dataPurpose": "consumed",
                                "experimentStepID": "c1234",
                                "role": "input",
                                "id": "c1",
                            },
                        ),
                    ],
                ),
            ],
        )

        obj = Infrastructure.load_xml(xml)
