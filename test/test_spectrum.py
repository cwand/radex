import unittest
import radex
import numpy as np
import datetime


class TestSpectrum(unittest.TestCase):

	def test_rate_by_kev_copied(self):
		c1 = np.arange(6, dtype=float).reshape(-1, 2)
		t1 = 100
		d1 = datetime.date(2020, 2, 1)
		spec1 = radex.Spectrum(c1, t1, d1)
		c1[2, 1] = 100
		self.assertEqual(spec1.rate_by_kev[2, 1], 5)

	def test_rate_by_kev_correct_size(self):
		c1 = np.zeros((4, 3))
		c2 = np.zeros((1, 2, 3))
		t1 = 100
		d1 = datetime.date(2020, 2, 1)
		self.assertRaises(ValueError, radex.Spectrum, c1, t1, d1)
		self.assertRaises(ValueError, radex.Spectrum, c2, t1, d1)

	def test_add_spectrum(self):
		c1 = np.arange(6, dtype=float).reshape(-1, 2)
		t1 = 100
		d1 = datetime.date(2020, 2, 1)
		c2 = np.arange(6, dtype=float).reshape(-1, 2)
		t2 = 100
		d2 = datetime.date(2020, 2, 1)
		spec1 = radex.Spectrum(c1, t1, d1)
		spec2 = radex.Spectrum(c2, t2, d2)
		spec12 = radex.add_spectrum(spec1, spec2)
		np.testing.assert_array_equal(np.array([0, 2, 4]), spec12.rate_by_kev[:, 0])
		np.testing.assert_array_equal(np.array([2, 6, 10]), spec12.rate_by_kev[:, 1])
		self.assertEqual(spec12.count_time, 100)
		self.assertEqual(spec12.mdate, datetime.date(2020, 2, 1))

	def test_add_spectrum_no_modification_to_input(self):
		c1 = np.arange(6, dtype=float).reshape(-1, 2)
		t1 = 100
		d1 = datetime.date(2020, 2, 1)
		c2 = np.arange(6, dtype=float).reshape(-1, 2)
		t2 = 100
		d2 = datetime.date(2020, 2, 1)
		spec1 = radex.Spectrum(c1, t1, d1)
		spec2 = radex.Spectrum(c2, t2, d2)
		radex.add_spectrum(spec1, spec2)
		np.testing.assert_array_equal(np.array([0, 2, 4]), spec1.rate_by_kev[:, 0])
		np.testing.assert_array_equal(np.array([1, 3, 5]), spec1.rate_by_kev[:, 1])
		np.testing.assert_array_equal(np.array([0, 2, 4]), spec2.rate_by_kev[:, 0])
		np.testing.assert_array_equal(np.array([1, 3, 5]), spec2.rate_by_kev[:, 1])

	def test_subtract_spectrum(self):
		c1 = np.arange(6, dtype=float).reshape(-1, 2)
		t1 = 100
		d1 = datetime.date(2020, 2, 1)
		c2 = np.arange(6, dtype=float).reshape(-1, 2)
		t2 = 100
		d2 = datetime.date(2020, 2, 1)
		spec1 = radex.Spectrum(c1, t1, d1)
		spec2 = radex.Spectrum(c2, t2, d2)
		spec12 = radex.subtract_spectrum(spec1, spec2)
		np.testing.assert_array_equal(np.array([0, 2, 4]), spec12.rate_by_kev[:, 0])
		np.testing.assert_array_equal(np.array([0, 0, 0]), spec12.rate_by_kev[:, 1])
		self.assertEqual(spec12.count_time, 100)
		self.assertEqual(spec12.mdate, datetime.date(2020, 2, 1))

	def test_subtract_spectrum_no_modification_to_input(self):
		c1 = np.arange(6, dtype=float).reshape(-1, 2)
		t1 = 100
		d1 = datetime.date(2020, 2, 1)
		c2 = np.arange(6, dtype=float).reshape(-1, 2)
		t2 = 100
		d2 = datetime.date(2020, 2, 1)
		spec1 = radex.Spectrum(c1, t1, d1)
		spec2 = radex.Spectrum(c2, t2, d2)
		radex.subtract_spectrum(spec1, spec2)
		np.testing.assert_array_equal(np.array([0, 2, 4]), spec1.rate_by_kev[:, 0])
		np.testing.assert_array_equal(np.array([1, 3, 5]), spec1.rate_by_kev[:, 1])
		np.testing.assert_array_equal(np.array([0, 2, 4]), spec2.rate_by_kev[:, 0])
		np.testing.assert_array_equal(np.array([1, 3, 5]), spec2.rate_by_kev[:, 1])

	def test_add_subtract_spectrum_error_bins(self):
		c1 = np.arange(6, dtype=float).reshape(-1, 2)
		t1 = 100
		c2 = np.arange(3, 9, dtype=float).reshape(-1, 2)
		t2 = 100
		spec1 = radex.Spectrum(c1, t1)
		spec2 = radex.Spectrum(c2, t2)
		self.assertRaises(ValueError, radex.add_spectrum, spec1, spec2)
		self.assertRaises(ValueError, radex.subtract_spectrum, spec1, spec2)

	def test_add_subtract_spectrum_error_time(self):
		c1 = np.arange(6, dtype=float).reshape(-1, 2)
		t1 = 90
		c2 = np.arange(6, dtype=float).reshape(-1, 2)
		t2 = 100
		spec1 = radex.Spectrum(c1, t1)
		spec2 = radex.Spectrum(c2, t2)
		self.assertRaises(ValueError, radex.add_spectrum, spec1, spec2)
		self.assertRaises(ValueError, radex.subtract_spectrum, spec1, spec2)

	def test_add_subtract_spectrum_error_date(self):
		c1 = np.arange(6, dtype=float).reshape(-1, 2)
		t1 = 100
		d1 = datetime.date(2010, 10, 24)
		c2 = np.arange(6, dtype=float).reshape(-1, 2)
		t2 = 100
		d2 = datetime.date(2010, 10, 25)
		spec1 = radex.Spectrum(c1, t1, d1)
		spec2 = radex.Spectrum(c2, t2, d2)
		self.assertRaises(ValueError, radex.add_spectrum, spec1, spec2)
		self.assertRaises(ValueError, radex.subtract_spectrum, spec1, spec2)

	def test_rate_in_window_specified(self):
		c1 = np.arange(10, dtype=float).reshape(-1, 2)
		t1 = 100
		spec1 = radex.Spectrum(c1, t1)
		self.assertEqual(spec1.window_rate((4, 7)), 12)

	def test_rate_in_window_full(self):
		c1 = np.arange(10, dtype=float).reshape(-1, 2)
		t1 = 100
		spec1 = radex.Spectrum(c1, t1)
		self.assertEqual(spec1.window_rate((0, 8)), 25)
