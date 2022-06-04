import unittest

from reamber.algorithms.generate.sv.SvSequence import SvSequence


class TestRescale(unittest.TestCase):

    def test(self):
        # Rescale Test
        seq = SvSequence([0, 1, 2])
        seq.rescale(0, 1000, inplace=True)

        self.assertAlmostEqual(seq[0].offset, 0)
        self.assertAlmostEqual(seq[1].offset, 500)
        self.assertAlmostEqual(seq[2].offset, 1000)


if __name__ == '__main__':
    unittest.main()
