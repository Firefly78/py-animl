import unittest
from typing import Optional
from xml.etree.ElementTree import Element

from simple_animl.core import Field, XmlModel
from simple_animl.core.base import XmlMeta, class_from_tag


class TestAnnotation(unittest.TestCase):
    def test_NoAnnotation(self):
        def f():
            class Model_B(XmlModel):
                name = Field.Attribute(default="")

        self.assertRaisesRegex(TypeError, "Field missing annotation:", f)


class TestFields(unittest.TestCase):
    def test_Create(self):
        class Model_A(XmlModel):
            name: str = Field.Attribute(default="")
            name2: Optional[str] = Field.Attribute(alias="name-2")
            name3: str = Field.Attribute(default="my-name-3")
            name4: str = Field.Attribute(default_factory=lambda: "my-name-4")

            more: Optional[XmlModel] = Field.Child()

            more2: Optional[str] = Field.Text()

        a = Model_A()

        # No exception - pass


class TestClassFromTag(unittest.TestCase):
    def test_GetClass(self):
        class T_GetClassClass(XmlModel):
            pass

        self.assertEqual(class_from_tag("T_GetClassClass"), T_GetClassClass)

    def test_GetClassFail_NoClass(self):
        self.assertRaisesRegex(
            ValueError, "Unable to find class with tag", class_from_tag, "T_NoClass"
        )

    def test_GetClassFail_MultipleClass(self):
        class T_MultiFailClass(XmlModel):
            pass

        class T_MultiFailClass(XmlModel):
            pass

        self.assertRaisesRegex(
            ValueError, "Multiple classes with tag", class_from_tag, "T_MultiFailClass"
        )


class TestDumpAttribute(unittest.TestCase):
    def test_Dump(self):
        class Model_A(XmlModel):
            name: str = Field.Attribute()

        xml = Model_A(name="my-name").dump_xml()

        self.assertTrue("name" in xml.attrib)
        self.assertEqual(xml.attrib["name"], "my-name")


class TestDumpChild(unittest.TestCase):
    def test_Dump(self):
        class Model_B(XmlModel):
            pass

        class Model_C(XmlModel):
            name: str = Field.Attribute()

        class Model_A(XmlModel):
            child: Model_B = Field.Child()
            child2: list[Model_C] = Field.Child(
                default=[
                    Model_C(name="C1"),
                    Model_C(name="C2"),
                ]
            )

        xml = Model_A(child=Model_B()).dump_xml()

        children = [x for x in xml]
        self.assertTrue(len(children) == 3)
        self.assertEqual(children[0].tag, "Model_B")
        self.assertEqual(children[1].tag, "Model_C")
        self.assertEqual(children[1].attrib["name"], "C1")
        self.assertEqual(children[2].tag, "Model_C")
        self.assertEqual(children[2].attrib["name"], "C2")


class TestDumpText(unittest.TestCase):
    def test_Dump(self):
        class Model_A(XmlModel):
            text: str = Field.Text()

        xml = Model_A(text="my-content").dump_xml()

        self.assertEqual(xml.text, "my-content")

    def test_DumpFail_MultipleText(self):
        def f():
            class Model_A(XmlModel):
                text: str = Field.Text(default="my-content")
                text2: str = Field.Text(default="my-content")

        self.assertRaisesRegex(Exception, "Only one text field allowed", f)


class TestLoadAttribute(unittest.TestCase):
    def test_Load(self):
        class T_Model_LoadAttribute(XmlModel):
            name: str = Field.Attribute()

        et = Element("T_Model_LoadAttribute", attrib={"name": "my-name"})
        model = T_Model_LoadAttribute.load_xml(et)
        self.assertEqual(model.name, "my-name")


class TestLoadChild(unittest.TestCase):
    def test_Load(self):
        class T_Model_LoadChildB(XmlModel):
            name: Optional[str] = Field.Attribute(default="my-name")

        class T_Model_LoadChild(XmlModel):
            child: T_Model_LoadChildB = Field.Child()

        et = Element("T_Model_LoadChild")
        et.append(Element("T_Model_LoadChildB"))
        model = T_Model_LoadChild.load_xml(et)
        self.assertTrue(model.child is not None)
        self.assertEqual(model.child.name, "my-name")


class TestLoadText(unittest.TestCase):
    def test_Load(self):
        class T_Model_LoadText(XmlModel):
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
        class GoodModel(XmlModel):
            pass

        self.assertEqual(GoodModel.tag, GoodModel.__name__)


class TestTag(unittest.TestCase):
    def test_CustomTag(self):
        class TagModel(XmlModel):
            tag = "mytag"

        self.assertEqual(TagModel().tag, "mytag")

    def test_DefaultTag(self):
        class TagModel(XmlModel):
            pass

        self.assertEqual(TagModel().tag, "TagModel")
