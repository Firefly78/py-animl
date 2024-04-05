import unittest
from typing import Optional
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

from helpers import create_dummy_regclass

from simple_animl.core import Field, XmlModel
from simple_animl.core.base import XmlMeta


class TestAnnotation(unittest.TestCase):
    def test_NoAnnotation(self):
        def f():
            class Model_B(XmlModel, regclass=create_dummy_regclass()):
                name = Field.Attribute(default="")

        self.assertRaisesRegex(TypeError, "Field missing annotation:", f)


class TestFields(unittest.TestCase):
    def test_Create(self):
        class Model_A4(XmlModel, regclass=create_dummy_regclass()):
            name: str = Field.Attribute(default="")
            name2: Optional[str] = Field.Attribute(alias="name-2")
            name3: str = Field.Attribute(default="my-name-3")
            name4: str = Field.Attribute(default_factory=lambda: "my-name-4")

            more: Optional[XmlModel] = Field.Child()

            more2: Optional[str] = Field.Text()

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

            class T_MultiFailClass(XmlModel, regclass=regclass):
                pass

            class T_MultiFailClass(XmlModel, regclass=regclass):
                pass

        self.assertRaisesRegex(
            ValueError, "Type 'T_MultiFailClass' already registered", f
        )


class TestCustomSerializer(unittest.TestCase):
    def test_DumpAttribute(self):
        class BoolDumpTest(XmlModel, regclass=create_dummy_regclass()):
            value: bool = Field.Attribute(
                on_serialize=lambda x: "true" if x else "false",
            )

        xml = BoolDumpTest(value=True).dump_xml()
        self.assertEqual(xml.attrib["value"], "true")

    def test_LoadAttribute(self):
        xml = '<BoolLoadTest value="true" />'

        class BoolLoadTest(XmlModel, regclass=create_dummy_regclass()):
            value: bool = Field.Attribute(
                on_deserialize=lambda x: x == "true",
            )

        model = BoolLoadTest.load_xml(ElementTree.fromstring(xml))
        self.assertEqual(model.value, True)

    def test_DumpText(self):
        class BoolDumpTest2(XmlModel, regclass=create_dummy_regclass()):
            value: str = Field.Text(on_serialize=lambda x: x + "-1")

        xml = BoolDumpTest2(value="hello").dump_xml()
        self.assertEqual(xml.text, "hello-1")

    def test_LoadText(self):
        xml = "<BoolLoadTest2>text</BoolLoadTest2>"

        class BoolLoadTest2(XmlModel, regclass=create_dummy_regclass()):
            value: str = Field.Text(on_deserialize=lambda x: x + "-2")

        model = BoolLoadTest2.load_xml(ElementTree.fromstring(xml))
        self.assertEqual(model.value, "text-2")


class TestDumpAttribute(unittest.TestCase):
    def test_Dump(self):
        class Model_AC(XmlModel, regclass=create_dummy_regclass()):
            name: str = Field.Attribute()

        xml = Model_AC(name="my-name").dump_xml()

        self.assertTrue("name" in xml.attrib)
        self.assertEqual(xml.attrib["name"], "my-name")


class TestDumpChild(unittest.TestCase):
    def test_Dump(self):
        regclass = create_dummy_regclass()

        class Model_B(XmlModel, regclass=regclass):
            pass

        class Model_C(XmlModel, regclass=regclass):
            name: str = Field.Attribute()

        class Model_A2(XmlModel, regclass=regclass):
            child: Model_B = Field.Child()
            child2: list[Model_C] = Field.Child(
                default=[
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
        class Model_A3(XmlModel, regclass=create_dummy_regclass()):
            text: str = Field.Text()

        xml = Model_A3(text="my-content").dump_xml()

        self.assertEqual(xml.text, "my-content")

    def test_DumpFail_MultipleText(self):
        def f():
            class Model_A(XmlModel, regclass=create_dummy_regclass()):
                text: str = Field.Text(default="my-content")
                text2: str = Field.Text(default="my-content")

        self.assertRaisesRegex(Exception, "Only one text field allowed", f)


class TestLoadAttribute(unittest.TestCase):
    def test_Load(self):
        class T_Model_LoadAttribute(XmlModel, regclass=create_dummy_regclass()):
            name: str = Field.Attribute()

        et = Element("T_Model_LoadAttribute", attrib={"name": "my-name"})
        model = T_Model_LoadAttribute.load_xml(et)
        self.assertEqual(model.name, "my-name")


class TestLoadChild(unittest.TestCase):
    def test_Load(self):
        regclass = create_dummy_regclass()

        class T_Model_LoadChildB(XmlModel, regclass=regclass):
            name: Optional[str] = Field.Attribute(default="my-name")

        class T_Model_LoadChild(XmlModel, regclass=regclass):
            child: T_Model_LoadChildB = Field.Child()

        et = Element("T_Model_LoadChild")
        et.append(Element("T_Model_LoadChildB"))
        model = T_Model_LoadChild.load_xml(et)
        self.assertTrue(model.child is not None)
        self.assertEqual(model.child.name, "my-name")


class TestLoadText(unittest.TestCase):
    def test_Load(self):
        class T_Model_LoadText(XmlModel, regclass=create_dummy_regclass()):
            text: Optional[str] = Field.Text()

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
        class TagModel(XmlModel, regclass=create_dummy_regclass()):
            tag = "mytag"

        self.assertEqual(TagModel().tag, "mytag")

    def test_DefaultTag(self):
        class TagModel_(XmlModel, regclass=create_dummy_regclass()):
            pass

        self.assertEqual(TagModel_().tag, "TagModel_")
