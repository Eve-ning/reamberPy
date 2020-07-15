import unittest
from math import sin, pi

from reamber.algorithms.generate.sv.generators.svOsuMeasureLineA import svOsuMeasureLineA
from reamber.algorithms.generate.sv.generators.svOsuMeasureLineB import svOsuMeasureLineB
from reamber.osu.OsuBpm import OsuBpm


class TestMeasureLine(unittest.TestCase):

    def testA(self):

        seq = svOsuMeasureLineA(firstOffset=5000,
                                lastOffset=20000,
                                funcs=[lambda x: 0.5 * sin(x * pi * 2),
                                       lambda x: 0.5 * sin(x * pi * 2 + pi)],
                                fillBpm=200, startX=0, endX=4, endBpm=200, referenceBpm=200,
                                paddingSize=20).combine()

        # with open("out.txt", "w+") as f:
        #     f.writelines([i.writeString() + "\n" for i in seq.writeAsBpm(OsuBpm)])

    def testB(self):

        lis = svOsuMeasureLineB(firstOffset=0,
                                lastOffset=40000,
                                funcs=[lambda x: 0.5 * sin(x * pi * 2),
                                       lambda x: 0.5 * sin(x * pi * 2 + pi)],
                                fillBpm=200, startX=0, endX=4, endBpm=100, referenceBpm=200,
                                paddingSize=20)

        # with open("out.txt", "w+") as f:
        #     f.writelines([i.writeString() + "\n" for i in lis])


if __name__ == '__main__':
    unittest.main()
