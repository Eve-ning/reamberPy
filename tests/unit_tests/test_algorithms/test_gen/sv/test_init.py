from reamber.algorithms.generate.sv.SvSequence import SvSequence, SvObj


def test_mixed_init():
    # Quick Init Mixed
    seq = SvSequence([100, (200, 2.0, True), (400, 3.0),
                      SvObj(offset=800, multiplier=5.0, fixed=True)])
    assert len(seq) == 4
