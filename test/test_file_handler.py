import unittest
import sys, os
import radex

class TestFileHandler(unittest.TestCase):


    def test_discover_descriptions(self):
        fh = radex.FileHandler('test/DICOM/')
        fh.discover()
        self.assertEqual(len(fh.descriptions()),3)
        self.assertTrue('10' in fh.descriptions())
        self.assertTrue('11' in fh.descriptions())
        self.assertTrue('12' in fh.descriptions())
        self.assertFalse('13' in fh.descriptions())

    def test_discover_filepaths(self):
        fh = radex.FileHandler('test/DICOM/')
        fh.discover()
        self.assertEqual(len(fh.files('10')),3)
        self.assertEqual(len(fh.files('10')),3)
        self.assertEqual(len(fh.files('12')),3)
        self.assertFalse(fh.files('13'))
        self.assertEqual(len(fh.descriptions()),3)
