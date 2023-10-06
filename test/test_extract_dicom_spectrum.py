import unittest

import radex
import os
from datetime import date


class TestExtractDicomSpectrum(unittest.TestCase):

	def test_extract_spectrum1(self):
		spectrum = radex.extract_spectrum(
			os.path.join('test', 'DICOM', 'PA1', 'ST1', 'SE1', '00000001.dcm'))
		self.assertEqual(spectrum.window_rate((0, 24)), 0.0)
		self.assertAlmostEqual(spectrum.window_rate((25, 25)), 0.00669, 5)
		self.assertAlmostEqual(spectrum.window_rate((78, 78)), 10.62427, 5)
		self.assertAlmostEqual(spectrum.window_rate((220, 220)), 2.72500, 5)
		self.assertAlmostEqual(spectrum.window_rate((431, 431)), 0.63690, 5)
		self.assertEqual(spectrum.window_rate((598, 599)), 0.0)
		self.assertEqual(spectrum.count_time, 300.0)
		self.assertEqual(spectrum.mdate, date(2020, 12, 30))

	def test_extract_sum_1and2(self):
		spectrum = radex.extract_sum([
			os.path.join('test', 'DICOM', 'PA1', 'ST1', 'SE1', '00000001.dcm'),
			os.path.join('test', 'DICOM', 'PA1', 'ST1', 'SE1', '00000002.dcm')
		])
		self.assertEqual(spectrum.window_rate((0, 24)), 0.0)
		self.assertAlmostEqual(spectrum.window_rate((25, 25)), 0.01003, 5)
		self.assertAlmostEqual(spectrum.window_rate((78, 78)), 30.38408, 5)
		self.assertAlmostEqual(spectrum.window_rate((220, 220)), 6.02162, 5)
		self.assertAlmostEqual(spectrum.window_rate((431, 431)), 1.38231, 5)
		self.assertEqual(spectrum.window_rate((598, 599)), 0.0)
		self.assertEqual(spectrum.count_time, 300.0)
		self.assertEqual(spectrum.mdate, date(2020, 12, 30))
