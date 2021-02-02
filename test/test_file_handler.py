import unittest
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import file_handler

class TestFileHandler(unittest.TestCase):

    def test_no_descriptions_after_init(self):
        fh = file_handler.FileHandler("")
        self.assertFalse(fh.get_descriptions())

    def test_discover_descriptions(self):
        dirname = os.path.dirname(os.path.abspath(__file__))+"\\DICOM\\"
        fh = file_handler.FileHandler(dirname)
        fh.discover()
        self.assertEqual(len(fh.get_descriptions()),3)
        self.assertTrue('10' in fh.get_descriptions())
        self.assertTrue('11' in fh.get_descriptions())
        self.assertTrue('12' in fh.get_descriptions())
        self.assertFalse('13' in fh.get_descriptions())

    def test_discover_filepaths(self):
        dirname = os.path.dirname(os.path.abspath(__file__))+"\\DICOM\\"
        fh = file_handler.FileHandler(dirname)
        fh.discover()
        self.assertEqual(len(fh.get_files_for_description('10')),3)
        self.assertEqual(len(fh.get_files_for_description('10')),3)
        self.assertEqual(len(fh.get_files_for_description('12')),3)
        self.assertFalse(fh.get_files_for_description('13'))
        self.assertEqual(len(fh.get_descriptions()),3)
