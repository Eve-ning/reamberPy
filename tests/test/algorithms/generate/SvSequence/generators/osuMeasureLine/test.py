import unittest

# Test Funcs
# Bounce
# return 100000 * (abs(sin(10 * x * pi) / 3) + x / 3) + 2000
# Wobble
# return 15000 * ((sin(x * 2 * pi) + 1) * sin(x * 4 * pi) * sin(x * 32 * pi) + 2) + 5000
from reamber.algorithms.generate.sv.SvPkg import SvPkg
from reamber.algorithms.generate.sv.generators.svOsuMeasureLine import svOsuMeasureLine, svOsuMeasureLine2
from reamber.osu.OsuBpmObj import OsuBpmObj
from math import sin, pi, cos


class TestMeasureLine(unittest.TestCase):

    def test(self):

        def f(x: float): return 40000 * (sin(x * 2 * pi) + 1.1)
        def g(x: float): return 40000 * (sin(x * 2 * pi + pi) + 1.1)

        seq = svOsuMeasureLine(firstOffset=1000,
                               lastOffset=3000,
                               funcs=[f,g]).combine(SvPkg.CombineMethod.DROP_BY_POINT, combineMethodWindow=0)
        seqR = SvPkg.repeat(seq, 5).combine(SvPkg.CombineMethod.DROP_BY_POINT, combineMethodWindow=0)

        seqR[-1].multiplier = 191.0

        with open("out.txt", "w+") as f:
            for bpm in seqR.writeAsBpm(OsuBpmObj, metronome=999):
                assert isinstance(bpm, OsuBpmObj)
                f.write(bpm.writeString() + '\n')

    def test2(self):

        def f(x: float): return 10000 * (sin(x * 2 * pi)              + 1) + 5000
        def g(x: float): return 10000 * (sin(x * 2 * pi + 1 * pi / 6) + 1) + 5000
        def h(x: float): return 10000 * (sin(x * 2 * pi + 2 * pi / 6) + 1) + 5000
        def i(x: float): return 10000 * (sin(x * 2 * pi + 3 * pi / 6) + 1) + 5000
        def j(x: float): return 10000 * (sin(x * 2 * pi + 4 * pi / 6) + 1) + 5000
        def k(x: float): return 10000 * (sin(x * 2 * pi + 5 * pi / 6) + 1) + 5000

        seq = svOsuMeasureLine2(firstOffset=1000,
                                lastOffset=8000,
                                paddingSize=25,
                                funcs=[f,g,h,i,j,k]).combine(SvPkg.CombineMethod.DROP_BY_POINT, combineMethodWindow=0)
        seqR = SvPkg.repeat(seq, 5).combine(SvPkg.CombineMethod.DROP_BY_POINT, combineMethodWindow=0)

        seqR[-1].multiplier = 191.0

        with open("out2.txt", "w+") as f:
            for bpm in seqR.writeAsBpm(OsuBpmObj, metronome=999):
                assert isinstance(bpm, OsuBpmObj)
                f.write(bpm.writeString() + '\n')


if __name__ == '__main__':
    unittest.main()
