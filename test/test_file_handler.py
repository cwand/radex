import unittest
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import file_handler

class TestFileHandler(unittest.TestCase):

    def test_no_descriptions_after_init(self):
        fh = file_handler.FileHandler("")
        self.assertFalse(fh.getDescriptions())

    def test_discover_descriptions(self):
        dirname = os.path.dirname(os.path.abspath(__file__))+"\\DICOM\\"
        fh = file_handler.FileHandler(dirname)
        fh.discover()
        self.assertEqual(len(fh.getDescriptions()),3)
        self.assertTrue('10' in fh.getDescriptions())
        self.assertTrue('11' in fh.getDescriptions())
        self.assertTrue('12' in fh.getDescriptions())
        self.assertFalse('13' in fh.getDescriptions())

    def test_discover_filepaths(self):
        dirname = os.path.dirname(os.path.abspath(__file__))+"\\DICOM\\"
        fh = file_handler.FileHandler(dirname)
        fh.discover()
        self.assertEqual(len(fh.getFilesForDescription('10')),3)
        self.assertEqual(len(fh.getFilesForDescription('10')),3)
        self.assertEqual(len(fh.getFilesForDescription('12')),3)
        self.assertFalse(fh.getFilesForDescription('13'))
        self.assertEqual(len(fh.getDescriptions()),3)
