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
        osu = OsuMap.read_file(OSU_CARAVAN)

        qua = OsuToQua.convert(osu)
        qua.write_file("caravan.qua")

    # @profile
    def test_osu2(self):
        # Stops
        osu = OsuMap.read_file(OSU_ESCAPES)

        qua = OsuToQua.convert(osu)
        qua.write_file("escapes.qua")

    # @profile
    def test_osu3(self):
        # Complex BPM
        osu = OsuMap.read_file(OSU_GRAVITY)

        qua = OsuToQua.convert(osu)
        qua.write_file("gravity.qua")


if __name__ == '__main__':
    unittest.main()
