import unittest
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils
import datetime

class TestUtilsYYYYMMDD2Date(unittest.TestCase):

	def test_yyyymmdd2date(self):
		d = datetime.date(2000,10,14)
		ds = '20001014'
		self.assertEqual(d,utils.yyyymmdd2date(ds))


class TestUtilsWeightedMean(unittest.TestCase):

	def test_wmean(self):
		x = [(10,1),(12.5,2),(15,1.5)]
		res = utils.wmean(x)

		self.assertEqual(res[0],11.6803278688525)
		self.assertEqual(res[0],1.62305715268227)
