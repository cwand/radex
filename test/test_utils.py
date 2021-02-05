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
