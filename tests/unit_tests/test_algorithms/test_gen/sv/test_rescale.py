from reamber.algorithms.generate.sv.SvSequence import SvSequence


def test_rescale():
    seq = SvSequence([100, 200, 60, 400])
    seq.rescale(300, 800, inplace=True)
