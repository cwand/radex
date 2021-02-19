import unittest
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import spectrum
import activity
import numpy as np


class TestActivityMDAAnalysis(unittest.TestCase):

		def test_mda_analysis(self):
			bkg = np.arange(10).reshape(-1,2)
			src = np.arange(10).reshape(-1,2)
			src[:,1] *= 5
			src_bkg = np.arange(10).reshape(-1,2)
			src_bkg[:,1] *= 2
			t1 = 4
			spec_bkg = spectrum.Spectrum(bkg,t1)
			spec_src = spectrum.Spectrum(src,t1)
			spec_src_bkg = spectrum.Spectrum(src_bkg,t1)
			mda = activity.mda_analysis(spec_bkg, spec_src, spec_src_bkg, 100.0, (2,6))

			self.assertAlmostEqual(mda.sens, 0.45)
			self.assertAlmostEqual(mda.dsens, 0.051234753829798)
			self.assertAlmostEqual(mda.mda, 12.909944487358057)
			self.assertAlmostEqual(mda.dmda, 1.689656258416172)





class TestActivityMDASimple(unittest.TestCase):

    def test_mda_simple_with_sensitivity_and_window(self):
        c1 = np.arange(10).reshape(-1,2)
        t1 = 1
        spec1 = spectrum.Spectrum(c1,t1)
        self.assertEqual(activity.mda_simple(spec1,0.5,[0,4]),18)

    def test_mda_simple_without_sensitivity_and_window(self):
        c1 = np.arange(10).reshape(-1,2)
        t1 = 1
        spec1 = spectrum.Spectrum(c1,t1)
        self.assertEqual(activity.mda_simple(spec1),15)


class TestActivityDecay(unittest.TestCase):

    def test_decay(self):
        self.assertEqual(activity.decay(200,100,5),5)
        self.assertEqual(activity.decay(400,100,4),8)
