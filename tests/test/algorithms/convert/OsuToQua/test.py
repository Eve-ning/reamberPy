import unittest

from reamber.algorithms.convert.OsuToQua import OsuToQua
from reamber.osu.OsuMap import OsuMap
from tests.test.RSC_PATHS import *


# import logging
#
# logging.basicConfig(filename="event.log", filemode="w+", level=logging.DEBUG)


class TestOsuToQua(unittest.TestCase):

    # @profile
    def test_osu1(self):
        # Complex BPM Points
        osu = OsuMap.readFile(OSU_CARAVAN)

        qua = OsuToQua.convert(osu)
        # qua.writeFile("out.qua")

    # @profile
    def test_osu2(self):
        # Stops
        osu = OsuMap.readFile(OSU_ESCAPES)

        qua = OsuToQua.convert(osu)
        # qua.writeFile("out.qua")

    # @profile
    def test_osu3(self):
        # Complex BPM
        osu = OsuMap.readFile(OSU_GRAVITY)

        qua = OsuToQua.convert(osu)
        qua.music = "Gravity.mp3"
        # qua.writeFile("out.qua")


if __name__ == '__main__':
    unittest.main()
