import unittest
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import spectrum
import numpy as np

class TestSpectrum(unittest.TestCase):

    def test_add_spectrum(self):
        c1 = np.arange(6).reshape(-1,2)
        t1 = 100
        c2 = np.arange(6).reshape(-1,2)
        t2 = 100
        spec1 = spectrum.Spectrum(c1,t1)
        spec2 = spectrum.Spectrum(c2,t2)
        spec12 = spectrum.add(spec1,spec2)
        np.testing.assert_array_equal(np.array([0,2,4]),spec12.rate_by_kev[:,0])
        np.testing.assert_array_equal(np.array([2,6,10]),spec12.rate_by_kev[:,1])
        self.assertEqual(spec12.count_time,100)

    def test_subtract_spectrum(self):
        c1 = np.arange(6).reshape(-1,2)
        t1 = 100
        c2 = np.arange(6).reshape(-1,2)
        t2 = 100
        spec1 = spectrum.Spectrum(c1,t1)
        spec2 = spectrum.Spectrum(c2,t2)
        spec12 = spectrum.subtract(spec1,spec2)
        np.testing.assert_array_equal(np.array([0,2,4]),spec12.rate_by_kev[:,0])
        np.testing.assert_array_equal(np.array([0,0,0]),spec12.rate_by_kev[:,1])
        self.assertEqual(spec12.count_time,100)

    def test_add_subtract_spectrum_error(self):
        c1 = np.arange(6).reshape(-1,2)
        t1 = 100
        c2 = np.arange(3,9).reshape(-1,2)
        t2 = 100
        spec1 = spectrum.Spectrum(c1,t1)
        spec2 = spectrum.Spectrum(c2,t2)
        self.assertRaises(ValueError, spectrum.add, spec1, spec2)
        self.assertRaises(ValueError, spectrum.subtract, spec1, spec2)

    def test_add_subtract_spectrum_error2(self):
        c1 = np.arange(6).reshape(-1,2)
        t1 = 90
        c2 = np.arange(6).reshape(-1,2)
        t2 = 100
        spec1 = spectrum.Spectrum(c1,t1)
        spec2 = spectrum.Spectrum(c2,t2)
        self.assertRaises(ValueError, spectrum.add, spec1, spec2)
        self.assertRaises(ValueError, spectrum.subtract, spec1, spec2)

    def test_rate_in_window_specified(self):
        c1 = np.arange(10).reshape(-1,2)
        t1 = 100
        spec1 = spectrum.Spectrum(c1,t1)
        self.assertEqual(spec1.window_rate([4,7]),12)

    def test_rate_in_window_full(self):
        c1 = np.arange(10).reshape(-1,2)
        t1 = 100
        spec1 = spectrum.Spectrum(c1,t1)
        self.assertEqual(spec1.window_rate(),25)
