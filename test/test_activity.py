import unittest
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import spectrum
import activity
import numpy as np



class TestActivityDecay(unittest.TestCase):

    def test_decay(self):
        self.assertEqual(activity.decay(200,100,5),5)
        self.assertEqual(activity.decay(400,100,4),8)
