import unittest
from reamber.algorithms.generate.sv.SvSequence import SvSequence


class TestSvSequence(unittest.TestCase):

    def test10(self):
        # Norm Test
        seq = SvSequence([0, (500, 1.5, True), 1000])
        seq.appendInit([1,2,3])
        print(seq)
        pass


if __name__ == '__main__':
    unittest.main()
