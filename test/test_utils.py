import unittest
import radex
import datetime


class TestUtilsYYYYMMDD2Date(unittest.TestCase):

	def test_yyyymmdd2date(self):
		d = datetime.date(2000, 10, 14)
		ds = '20001014'
		self.assertEqual(d, radex.yyyymmdd2date(ds))
