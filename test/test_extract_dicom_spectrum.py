import unittest
import radex
import os


class TestExtractDicomSpectrum(unittest.TestCase):

	def test_decay(self):
		spectrum = radex.extract_spectrum(
			os.path.join('test', 'DICOM', 'PA1', 'ST1', 'SE1', '00000001.dcm'))
		print(spectrum.rate_by_kev)
		self.assertFalse(True)


