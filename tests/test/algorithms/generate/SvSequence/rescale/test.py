import unittest
from reamber.algorithms.generate.sv.SvSequence import SvSequence,SvObj
from reamber.algorithms.generate.sv.SvPkg import SvPkg


class TestSvSequence(unittest.TestCase):

    def test(self):
        # Quick Init Mixed
        seq = SvSequence([100, 200, 60, 400])
        seq.rescale(300, 800, inplace=True)


        pass


if __name__ == '__main__':
    unittest.main()
