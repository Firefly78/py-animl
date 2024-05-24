import unittest
from dataclasses import dataclass, field
from typing import Annotated, Optional
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

from helpers import create_dummy_regclass

from animl2.core import ATTRIB, CHILD, TEXT, XmlModel
from animl2.core.base import XmlMeta


class TestFields(unittest.TestCase):
    def test_Create(self):
        @dataclass
        class Model_A4(XmlModel, regclass=create_dummy_regclass()):
            name: Annotated[str, ATTRIB] = ""
            name2: Annotated[Optional[str], ATTRIB(alias="name-2")] = None
            name3: Annotated[str, ATTRIB] = "my-name-3"
            name4: Annotated[str, ATTRIB] = field(default_factory=lambda: "my-name-4")

            more: Annotated[Optional[XmlModel], CHILD] = None

            more2: Annotated[Optional[str], TEXT] = None

        a = Model_A4()

        # No exception - pass


class TestClassFromTag(unittest.TestCase):
    def test_GetClass(self):
        class T_GetClassClass(XmlModel, regclass=create_dummy_regclass()):
            pass

        self.assertEqual(
            T_GetClassClass.class_from_tag("T_GetClassClass"), T_GetClassClass
        )

    def test_GetClassFail_NoClass(self):
        class ModelA(XmlModel, regclass=create_dummy_regclass()):
            pass

        self.assertRaisesRegex(
            ValueError,
            "Unable to find class with tag",
            ModelA.class_from_tag,
            "T_NoClass",
        )

    def test_GetClassFail_MultipleClass(self):
        def f():
            regclass = create_dummy_regclass()

            @dataclass
            class T_MultiFailClass(XmlModel, regclass=regclass):
                a: Annotated[str, ATTRIB]

            @dataclass
            class T_MultiFailClassA(XmlModel, regclass=regclass):
                tag = "T_MultiFailClass"
                b: Annotated[str, ATTRIB]

        self.assertRaisesRegex(
            ValueError, "Type 'T_MultiFailClass' already registered", f
        )


class TestCustomSerializer(unittest.TestCase):
    def test_DumpAttribute(self):
        @dataclass
        class BoolDumpTest(XmlModel, regclass=create_dummy_regclass()):
            value: Annotated[
                bool, ATTRIB(on_serialize=lambda x: "true" if x else "false")
            ]

        xml = BoolDumpTest(value=True).dump_xml()
        self.assertEqual(xml.attrib["value"], "true")

    def test_LoadAttribute(self):
        xml = '<BoolLoadTest value="true" />'

        @dataclass
        class BoolLoadTest(XmlModel, regclass=create_dummy_regclass()):
            value: Annotated[bool, ATTRIB(on_deserialize=lambda x: x == "true")]

        model = BoolLoadTest.load_xml(ElementTree.fromstring(xml))
        self.assertEqual(model.value, True)

    def test_DumpText(self):
        @dataclass
        class BoolDumpTest2(XmlModel, regclass=create_dummy_regclass()):
            value: Annotated[str, TEXT(on_serialize=lambda x: x + "-1")]

        xml = BoolDumpTest2(value="hello").dump_xml()
        self.assertEqual(xml.text, "hello-1")

    def test_LoadText(self):
        xml = "<BoolLoadTest2>text</BoolLoadTest2>"

        @dataclass
        class BoolLoadTest2(XmlModel, regclass=create_dummy_regclass()):
            value: Annotated[str, TEXT(on_deserialize=lambda x: x + "-2")]

        model = BoolLoadTest2.load_xml(ElementTree.fromstring(xml))
        self.assertEqual(model.value, "text-2")


class TestDumpAttribute(unittest.TestCase):
    def test_Dump(self):
        @dataclass
        class Model_AC(XmlModel, regclass=create_dummy_regclass()):
            name: Annotated[str, ATTRIB]

        xml = Model_AC(name="my-name").dump_xml()

        self.assertTrue("name" in xml.attrib)
        self.assertEqual(xml.attrib["name"], "my-name")


class TestDumpChild(unittest.TestCase):
    def test_Dump(self):
        regclass = create_dummy_regclass()

        @dataclass
        class Model_B(XmlModel, regclass=regclass):
            pass

        @dataclass
        class Model_C(XmlModel, regclass=regclass):
            name: Annotated[str, ATTRIB]

        @dataclass
        class Model_A2(XmlModel, regclass=regclass):
            child: Annotated[Optional[Model_B], CHILD]
            child2: Annotated[
                list[Model_C],
                CHILD,
            ] = field(
                default_factory=lambda: [
                    Model_C(name="C1"),
                    Model_C(name="C2"),
                ]
            )

        xml = Model_A2(child=Model_B()).dump_xml()

        children = [x for x in xml]
        self.assertTrue(len(children) == 3)
        self.assertEqual(children[0].tag, "Model_B")
        self.assertEqual(children[1].tag, "Model_C")
        self.assertEqual(children[1].attrib["name"], "C1")
        self.assertEqual(children[2].tag, "Model_C")
        self.assertEqual(children[2].attrib["name"], "C2")


class TestDumpText(unittest.TestCase):
    def test_Dump(self):

        @dataclass
        class Model_A3(XmlModel, regclass=create_dummy_regclass()):
            text: Annotated[str, TEXT]

        xml = Model_A3(text="my-content").dump_xml()

        self.assertEqual(xml.text, "my-content")

    def test_DumpFail_MultipleText(self):

        @dataclass
        class Model_A(XmlModel, regclass=create_dummy_regclass()):
            text: Annotated[str, TEXT] = field(default="my-content")
            text2: Annotated[str, TEXT] = field(default="my-content")

        self.assertRaisesRegex(Exception, "Only one text field allowed", Model_A)


class TestLoadAttribute(unittest.TestCase):
    def test_Load(self):
        @dataclass
        class T_Model_LoadAttribute(XmlModel, regclass=create_dummy_regclass()):
            name: Annotated[str, ATTRIB]

        et = Element("T_Model_LoadAttribute", attrib={"name": "my-name"})
        model = T_Model_LoadAttribute.load_xml(et)
        self.assertEqual(model.name, "my-name")


class TestLoadChild(unittest.TestCase):
    def test_Load(self):
        regclass = create_dummy_regclass()

        @dataclass
        class T_Model_LoadChildB(XmlModel, regclass=regclass):
            name: Annotated[Optional[str], ATTRIB] = field(default="my-name")

        @dataclass
        class T_Model_LoadChild(XmlModel, regclass=regclass):
            child: Annotated[T_Model_LoadChildB, CHILD]

        et = Element("T_Model_LoadChild")
        et.append(Element("T_Model_LoadChildB"))
        model = T_Model_LoadChild.load_xml(et)
        self.assertTrue(model.child is not None)
        self.assertEqual(model.child.name, "my-name")


class TestLoadText(unittest.TestCase):
    def test_Load(self):
        @dataclass
        class T_Model_LoadText(XmlModel, regclass=create_dummy_regclass()):
            text: Annotated[Optional[str], TEXT]

        et = Element("T_Model_LoadText")
        et.text = "my-content"
        model = T_Model_LoadText.load_xml(et)
        self.assertEqual(model.text, "my-content")


class TestMeta(unittest.TestCase):
    def test_FaultyMeta(self):
        def define_model():
            class BadModel(metaclass=XmlMeta):
                pass

        self.assertRaises(TypeError, define_model)

    def test_GoodMeta(self):
        class GoodModel(XmlModel, regclass=create_dummy_regclass()):
            pass

        self.assertEqual(GoodModel.tag, GoodModel.__name__)


class TestTag(unittest.TestCase):
    def test_CustomTag(self):
        @dataclass
        class TagModel(XmlModel, regclass=create_dummy_regclass()):
            tag = "mytag"

        self.assertEqual(TagModel().tag, "mytag")

    def test_DefaultTag(self):
        @dataclass
        class TagModel_(XmlModel, regclass=create_dummy_regclass()):
            pass

        self.assertEqual(TagModel_().tag, "TagModel_")
