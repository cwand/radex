import unittest
import sys, os
import radex
import datetime
import numpy as np


class TestSpectrumAnalysisModel(unittest.TestCase):

	def test_no_background_critical_level_and_detection_limit_error(self):

		s = radex.SpectrumAnalysisModel()
		self.assertRaises(AttributeError, s.critical_level)
		self.assertRaises(AttributeError, s.detection_limit)


	def test_zero_background_critlvl_detlim(self):

		s = radex.SpectrumAnalysisModel()

		c1 = np.zeros((4,2)) # cps
		c1[0,0] = 0; c1[1,0] = 1; c1[2,0] = 2; c1[3,0] = 3
		c1[0,1] = 0; c1[1,1] = 0; c1[2,1] = 0; c1[3,1] = 0
		bkg = radex.Spectrum(c1,10,datetime.date(2020,2,1))

		s.set_background(bkg)
		self.assertEqual(s.critical_level(), 0)
		self.assertAlmostEqual(s.detection_limit(), 0.270554345409541)


	def test_nonzero_background_critlvl_detlim(self):

		s = radex.SpectrumAnalysisModel()

		c1 = np.zeros((4,2)) # cps
		c1[0,0] = 0; c1[1,0] = 1; c1[2,0] = 2; c1[3,0] = 3
		c1[0,1] = 1; c1[1,1] = 3; c1[2,1] = 7; c1[3,1] = 2
		bkg = radex.Spectrum(c1,10,datetime.date(2020,2,1))

		s.set_windows([(1,2)])

		s.set_background(bkg)
		self.assertAlmostEqual(s.critical_level(), 2.32617430735335)
		self.assertAlmostEqual(s.detection_limit(), 4.92290296011623)


	def test_no_spectrum_analysis_error(self):

		s = radex.SpectrumAnalysisModel()

		c1 = np.zeros((4,2)) # cps
		c1[0,0] = 0; c1[1,0] = 1; c1[2,0] = 2; c1[3,0] = 3
		c1[0,1] = 0; c1[1,1] = 0; c1[2,1] = 0; c1[3,1] = 0
		bkg = radex.Spectrum(c1,10,datetime.date(2020,2,1))
		s.set_background(bkg)

		self.assertRaises(AttributeError, s.analyse_spectrum)


	def test_background_gross_not_equal_time_error(self):

		s = radex.SpectrumAnalysisModel()

		c1 = np.zeros((4,2)) # cps
		c1[0,0] = 0; c1[1,0] = 1; c1[2,0] = 2; c1[3,0] = 3
		c1[0,1] = 1; c1[1,1] = 3; c1[2,1] = 7; c1[3,1] = 2
		bkg = radex.Spectrum(c1,10,datetime.date(2020,2,1))
		s.set_background(bkg)

		c2 = np.zeros((4,2)) # cps
		c2[0,0] = 0; c2[1,0] = 1; c2[2,0] = 2; c2[3,0] = 3
		c2[0,1] = 1; c2[1,1] = 3; c2[2,1] = 7; c2[3,1] = 2
		spc = radex.Spectrum(c2,11,datetime.date(2020,2,1))
		s.set_spectrum(spc)

		s.set_windows([(1,2)])

		self.assertRaises(ValueError, s.analyse_spectrum)


	def test_background_gross_not_equal_date_error(self):

		s = radex.SpectrumAnalysisModel()

		c1 = np.zeros((4,2)) # cps
		c1[0,0] = 0; c1[1,0] = 1; c1[2,0] = 2; c1[3,0] = 3
		c1[0,1] = 1; c1[1,1] = 3; c1[2,1] = 7; c1[3,1] = 2
		bkg = radex.Spectrum(c1,10,datetime.date(2020,2,1))
		s.set_background(bkg)

		c2 = np.zeros((4,2)) # cps
		c2[0,0] = 0; c2[1,0] = 1; c2[2,0] = 2; c2[3,0] = 3
		c2[0,1] = 1; c2[1,1] = 3; c2[2,1] = 7; c2[3,1] = 2
		spc = radex.Spectrum(c2,10,datetime.date(2020,2,2))
		s.set_spectrum(spc)

		s.set_windows([(1,2)])

		self.assertRaises(ValueError, s.analyse_spectrum)


	def test_background_gross_equal_analysis(self):

		s = radex.SpectrumAnalysisModel()

		c1 = np.zeros((4,2)) # cps
		c1[0,0] = 0; c1[1,0] = 1; c1[2,0] = 2; c1[3,0] = 3
		c1[0,1] = 1; c1[1,1] = 3; c1[2,1] = 7; c1[3,1] = 2
		bkg = radex.Spectrum(c1,10,datetime.date(2020,2,1))
		s.set_background(bkg)

		c2 = np.zeros((4,2)) # cps
		c2[0,0] = 0; c2[1,0] = 1; c2[2,0] = 2; c2[3,0] = 3
		c2[0,1] = 1; c2[1,1] = 3; c2[2,1] = 7; c2[3,1] = 2
		spc = radex.Spectrum(c2,10,datetime.date(2020,2,1))
		s.set_spectrum(spc)

		s.set_windows([(1,2)])

		res = s.analyse_spectrum()
		self.assertFalse(res.detected)
		self.assertAlmostEqual(res.net_signal, 0.0)
		self.assertAlmostEqual(res.conf, 2.32617430735335)

	def test_gross_lt_lc_analysis(self):

		s = radex.SpectrumAnalysisModel()

		c1 = np.zeros((4,2)) # cps
		c1[0,0] = 0; c1[1,0] = 1; c1[2,0] = 2; c1[3,0] = 3
		c1[0,1] = 1; c1[1,1] = 3; c1[2,1] = 7; c1[3,1] = 2
		bkg = radex.Spectrum(c1,10,datetime.date(2020,2,1))
		s.set_background(bkg)

		c2 = np.zeros((4,2)) # cps
		c2[0,0] = 0; c2[1,0] = 1; c2[2,0] = 2; c2[3,0] = 3
		c2[0,1] = 1; c2[1,1] = 4; c2[2,1] = 8; c2[3,1] = 2
		spc = radex.Spectrum(c2,10,datetime.date(2020,2,1))
		s.set_spectrum(spc)

		s.set_windows([(1,2)])

		res = s.analyse_spectrum()
		self.assertFalse(res.detected)
		self.assertAlmostEqual(res.net_signal, 2.0)
		self.assertAlmostEqual(res.conf, 2.43971219593826)


	def test_gross_gt_lc_analysis(self):

		s = radex.SpectrumAnalysisModel()

		c1 = np.zeros((4,2)) # cps
		c1[0,0] = 0; c1[1,0] = 1; c1[2,0] = 2; c1[3,0] = 3
		c1[0,1] = 1; c1[1,1] = 3; c1[2,1] = 7; c1[3,1] = 2
		bkg = radex.Spectrum(c1,10,datetime.date(2020,2,1))
		s.set_background(bkg)

		c2 = np.zeros((4,2)) # cps
		c2[0,0] = 0; c2[1,0] = 1; c2[2,0] = 2; c2[3,0] = 3
		c2[0,1] = 1; c2[1,1] = 13; c2[2,1] = 17; c2[3,1] = 2
		spc = radex.Spectrum(c2,10,datetime.date(2020,2,1))
		s.set_spectrum(spc)

		s.set_windows([(1,2)])

		res = s.analyse_spectrum()
		self.assertTrue(res.detected)
		self.assertAlmostEqual(res.net_signal, 20.0)
		self.assertAlmostEqual(res.conf, 3.91992796908011)


	def test_gross_lt_lc_sensitivity_analysis(self):

		s = radex.SpectrumAnalysisModel()

		c1 = np.zeros((4,2)) # cps
		c1[0,0] = 0; c1[1,0] = 1; c1[2,0] = 2; c1[3,0] = 3
		c1[0,1] = 1; c1[1,1] = 3; c1[2,1] = 7; c1[3,1] = 2
		bkg = radex.Spectrum(c1,10,datetime.date(2020,2,1))
		s.set_background(bkg)

		c2 = np.zeros((4,2)) # cps
		c2[0,0] = 0; c2[1,0] = 1; c2[2,0] = 2; c2[3,0] = 3
		c2[0,1] = 1; c2[1,1] = 4; c2[2,1] = 8; c2[3,1] = 2
		spc = radex.Spectrum(c2,10,datetime.date(2020,2,1))
		s.set_spectrum(spc)

		s.set_sensitivity(0.5,0.1)

		s.set_windows([(1,2)])

		res = s.analyse_spectrum()
		self.assertFalse(res.detected)
		self.assertAlmostEqual(res.net_signal, 4.0)
		self.assertAlmostEqual(res.conf, 5.05374417700982)


	def test_gross_gt_lc_analysis(self):

		s = radex.SpectrumAnalysisModel()

		c1 = np.zeros((4,2)) # cps
		c1[0,0] = 0; c1[1,0] = 1; c1[2,0] = 2; c1[3,0] = 3
		c1[0,1] = 1; c1[1,1] = 3; c1[2,1] = 7; c1[3,1] = 2
		bkg = radex.Spectrum(c1,10,datetime.date(2020,2,1))
		s.set_background(bkg)

		c2 = np.zeros((4,2)) # cps
		c2[0,0] = 0; c2[1,0] = 1; c2[2,0] = 2; c2[3,0] = 3
		c2[0,1] = 1; c2[1,1] = 13; c2[2,1] = 17; c2[3,1] = 2
		spc = radex.Spectrum(c2,10,datetime.date(2020,2,1))
		s.set_spectrum(spc)

		s.set_sensitivity(0.5,0.1)

		s.set_windows([(1,2)])

		res = s.analyse_spectrum()
		self.assertTrue(res.detected)
		self.assertAlmostEqual(res.net_signal, 40.0)
		self.assertAlmostEqual(res.conf, 17.5304508115316)
