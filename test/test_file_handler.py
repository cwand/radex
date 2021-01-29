import unittest
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import file_handler

class TestFileHandler(unittest.TestCase):

    def test_no_descriptions_after_init(self):
        fh = file_handler.FileHandler("")
        self.assertFalse(fh.getDescriptions(),
            "Should initially have no descriptions")

    def test_discover_descriptions(self):
        dirname = os.path.dirname(os.path.abspath(__file__))+"\\DICOM\\"
        fh = file_handler.FileHandler(dirname)
        fh.discover()
        self.assertEqual(len(fh.getDescriptions()),3,
            "Should contain three descriptions after discover")
        self.assertTrue('10' in fh.getDescriptions(),
            "Should contain the description '10'")
        self.assertTrue('11' in fh.getDescriptions(),
            "Should contain the description '11'")
        self.assertTrue('12' in fh.getDescriptions(),
            "Should contain the description '12'")
        self.assertFalse('13' in fh.getDescriptions(),
            "Should not contain the description '13'")

    def test_discover_filepaths(self):
        dirname = os.path.dirname(os.path.abspath(__file__))+"\\DICOM\\"
        fh = file_handler.FileHandler(dirname)
        fh.discover()
        self.assertEqual(len(fh.getFilesForDescription('10')),3,
            "Should contain three files for description '10'")
        self.assertEqual(len(fh.getFilesForDescription('10')),3,
            "Should contain three files for description '11'")
        self.assertEqual(len(fh.getFilesForDescription('12')),3,
            "Should contain three files for description '12'")
        self.assertFalse(fh.getFilesForDescription('13'),
            "Should contain no files for description '13'")
        self.assertEqual(len(fh.getDescriptions()),3,
            "Should contain three descriptions after asking about "
            "non-existing description")
