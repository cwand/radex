import unittest
import radex
import os


class TestFileHandler(unittest.TestCase):

    def test_default_to_config_file(self):
        fh = radex.FileHandler()
        self.assertEqual(fh.fp, 'train\\DICOM\\')

    def test_discover_descriptions(self):
        fh = radex.FileHandler(data_fp=os.path.join('test', 'DICOM'))
        fh.discover()
        self.assertEqual(len(fh.descriptions()), 3)
        self.assertTrue('10' in fh.descriptions())
        self.assertTrue('11' in fh.descriptions())
        self.assertTrue('12' in fh.descriptions())
        self.assertFalse('13' in fh.descriptions())

    def test_discover_filepaths(self):
        fh = radex.FileHandler(data_fp=os.path.join('test', 'DICOM'))
        fh.discover()
        self.assertEqual(len(fh.files('10')), 3)
        self.assertEqual(len(fh.files('11')), 3)
        self.assertEqual(len(fh.files('12')), 3)
        self.assertFalse(fh.files('13'))
