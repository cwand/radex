import unittest
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import count_statistics as cs
import numpy as np

class TestCountStatisticsSigmaRate(unittest.TestCase):
	def test_sigma_rate(self):
		rate = 100
		time = 4
		self.assertEqual(cs.sigma_rate(rate,time), 5.0)


class TestCountStatisticsSigmaRateBkg(unittest.TestCase):
	def test_sigma_rate_bkg(self):
		spl_rate = 242
		bkg_rate = 7
		time = 4
		self.assertEqual(cs.sigma_rate_bkg(spl_rate,bkg_rate,time), 8.0)
