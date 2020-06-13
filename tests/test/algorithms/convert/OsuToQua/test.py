import unittest
from tests.test.RSC_PATHS import *

from reamber.algorithms.convert.OsuToQua import OsuToQua
from reamber.osu.OsuMapObj import OsuMapObj
# import logging
#
# logging.basicConfig(filename="event.log", filemode="w+", level=logging.DEBUG)


class TestOsuToQua(unittest.TestCase):

    # @profile
    def test_osu1(self):
        # Complex BPM Points
        osu = OsuMapObj()
        osu.readFile("../../../../../" + OSU_CARAVAN)

        qua = OsuToQua.convert(osu)
        qua.writeFile("caravan.qua")

    # @profile
    def test_osu2(self):
        # Stops
        osu = OsuMapObj()
        osu.readFile("../../../../../" + OSU_ESCAPES)

        qua = OsuToQua.convert(osu)
        qua.writeFile("escapes.qua")

    # @profile
    def test_osu3(self):
        # Complex BPM
        osu = OsuMapObj()
        osu.readFile("../../../../../" + OSU_GRAVITY)

        qua = OsuToQua.convert(osu)
        qua.music = "Gravity.mp3"
        qua.writeFile("gravity.qua")


if __name__ == '__main__':
    unittest.main()
