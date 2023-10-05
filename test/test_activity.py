import unittest
import radex


class TestActivityDecay(unittest.TestCase):

    def test_decay(self):
        self.assertEqual(radex.decay(200, 100, 5), 5)
        self.assertEqual(radex.decay(400, 100, 4), 8)
