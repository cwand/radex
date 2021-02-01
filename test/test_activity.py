import unittest
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import spectrum
import activity
import numpy as np

class TestActivity(unittest.TestCase):

    def test_mda_simple_with_sensitivity_and_window(self):
        c1 = np.arange(10).reshape(-1,2)
        t1 = 1
        spec1 = spectrum.Spectrum(c1,t1)
        self.assertEqual(activity.mda_simple(spec1,0.5,[0,4]),18)
