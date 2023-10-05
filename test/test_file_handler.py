import unittest
import radex
import os


class TestFileHandler(unittest.TestCase):

    def test_discover_descriptions(self):
        fh = radex.FileHandler(data_fp=os.path.join('train', 'DICOM'))
        fh.discover()
        self.assertEqual(len(fh.descriptions()), 4)
        self.assertTrue('Bg' in fh.descriptions())
        self.assertTrue('1' in fh.descriptions())
        self.assertTrue('2' in fh.descriptions())
        self.assertFalse('3' in fh.descriptions())
        self.assertTrue('Bg2' in fh.descriptions())

    def test_discover_filepaths(self):
        fh = radex.FileHandler(data_fp=os.path.join('train', 'DICOM'))
        fh.discover()
        self.assertEqual(len(fh.files('Bg')), 3)
        self.assertEqual(len(fh.files('1')), 3)
        self.assertEqual(len(fh.files('2')), 3)
        self.assertFalse(fh.files('3'))
        self.assertEqual(len(fh.files('Bg2')), 3)
