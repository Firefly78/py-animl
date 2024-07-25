import unittest

from animl2 import AnIMLDoc, open_document


class Test_Version_090(unittest.TestCase):
    """
    Test a full scale example of the Version 0.9 model can be loaded and dumped.
    """

    def test_Load_Dump(self):
        with open("tests/resources/animl_0.90.xml") as f:
            doc = open_document(f)  # Success loading

        self.assertEqual(doc.version, "0.90")

        xml = doc.dump_xml()  # Success dumping
        self.assertEqual(xml.attrib["version"], "0.90")

        # And let's try reading it again
        doc = AnIMLDoc.load_xml(xml)
