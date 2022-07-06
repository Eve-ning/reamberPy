import unittest

from reamber.algorithms.generate.sv.SvPkg import SvPkg
from reamber.algorithms.generate.sv.SvSequence import SvSequence, SvObj


def test_copy_to():
    # Test Copy
    seq = SvSequence([SvObj(0, 1.0), SvObj(100, 2.0)])
    seqCopy = SvPkg.copy_to(seq=seq, offsets=[100, 200, 300]).combine(
        combine_method=SvPkg.CombineMethod.DROP_BY_POINT)
    assert len(seqCopy) == 4

