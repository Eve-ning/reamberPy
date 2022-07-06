import unittest

from reamber.algorithms.generate.sv.SvPkg import SvPkg
from reamber.algorithms.generate.sv.SvSequence import SvSequence, SvObj


def test_repeat():
    seq = SvSequence([SvObj(0, 1.0), SvObj(100, 2.0)])
    seq = SvPkg.repeat(seq, 4).combine(SvPkg.CombineMethod.DROP_BY_POINT)

    assert len(seq) == 5

