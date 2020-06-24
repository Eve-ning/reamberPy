import unittest
from reamber.algorithms.generate.sv.SvSequence import SvSequence
import logging

logging.basicConfig(filename="event.log", filemode="w+", level=logging.DEBUG)

class TestNormalize(unittest.TestCase):

    def testGeneric(self):
        seq = SvSequence([0, (500, 1.5, True), 1000])
        seq.normalizeTo(inplace=True)
        self.assertAlmostEqual(seq[0].multiplier, 0.5)

    def testComplex(self):
        seq = SvSequence([0, (500, 1.5, True), (700, 0.75, True), (800, 1.5, False), 1000])
        seq.normalizeTo(inplace=True)
        self.assertAlmostEqual(seq[0].multiplier, 0.78125)
        self.assertAlmostEqual(seq[3].multiplier, 1.171875)

    def testIgnoreFixed(self):
        seq = SvSequence([0, (500, 1.5, True), 1000])
        seq.normalizeTo(inplace=True, ignoreFixed=True)
        self.assertAlmostEqual(seq[0].multiplier, 0.8)
        self.assertAlmostEqual(seq[1].multiplier, 1.2)

    def testBadMin(self):
        seq = SvSequence([0, (500, 2.1, True), 1000])
        self.assertRaises(AssertionError, seq.normalizeTo, inplace=True, minAllowable=0)

    def testBadMax(self):
        # Norm Test
        seq = SvSequence([0, (500, 0.5, True), 1000])
        self.assertRaises(AssertionError, seq.normalizeTo, inplace=True, maxAllowable=1.2)


if __name__ == '__main__':
    unittest.main()
