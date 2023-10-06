import os.path
import unittest
import radex


class TestActivityDecay(unittest.TestCase):

    def test_decay(self):
        self.assertEqual(radex.decay(200, 100, 5), 5)
        self.assertEqual(radex.decay(400, 100, 4), 8)


class TestGetSens(unittest.TestCase):

    def test_get_sens(self):
        sens = radex.get_sens(os.path.join('test', 'sens.txt'))
        self.assertEqual(sens[(76, 89)], (0.198332758, 0.01))
        self.assertEqual(sens[(133, 165)], (0.198332758, 0.01))
        self.assertEqual(sens[(255, 283)], (0.198332758, 0.01))
        self.assertEqual(sens[(322, 366)], (0.198332758, 0.01))
        self.assertEqual(sens[(383, 422)], (0.198332758, 0.01))
