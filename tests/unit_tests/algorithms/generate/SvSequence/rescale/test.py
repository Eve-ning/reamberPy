import unittest

from reamber.algorithms.generate.sv.SvSequence import SvSequence


class TestSvSequence(unittest.TestCase):

    def test(self):
        # Quick Init Mixed
        seq = SvSequence([100, 200, 60, 400])
        seq.rescale(300, 800, inplace=True)


if __name__ == '__main__':
    unittest.main()
