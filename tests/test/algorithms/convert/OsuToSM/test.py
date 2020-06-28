import unittest
from tests.test.RSC_PATHS import *

from reamber.algorithms.convert.OsuToSM import OsuToSM
from reamber.osu.OsuMapObj import OsuMapObj
# import logging
#
# logging.basicConfig(filename="event.log", filemode="w+", level=logging.DEBUG)


class TestOsuToSM(unittest.TestCase):

    # # @profile
    # def test_osu1(self):
    #     # Complex BPM Points
    #     osu = OsuMapObj()
    #     osu.readFile(OSU_CARAVAN)
    #
    #     sm = OsuToSM.convert(osu)
    #     sm.offset -= 325 + 360
    #     sm.music = "caravan.mp3"
    #     sm.banner = "bn.png"
    #     sm.cdTitle = "cdtitle.png"
    #     sm.writeFile("out.sm", alignBpms=True)
    #
    # # @profile
    # def test_osu2(self):
    #     # Stops
    #     osu = OsuMapObj()
    #     osu.readFile(OSU_ESCAPES)
    #
    #     sm = OsuToSM.convert(osu)
    #     sm.offset -= 635 + 575
    #     sm.writeFile("out.sm", alignBpms=True)

    # @profile
    def test_osu3(self):
        # Complex BPM
        osu = OsuMapObj()
        osu.readFile(OSU_GRAVITY)

        sm = OsuToSM.convert(osu)
        sm.offset -= 15 + 41
        sm.music = "Gravity.mp3"
        sm.writeFile("out.sm", alignBpms=True, BEAT_ERROR_THRESHOLD=5.0, BEAT_CORRECTION_FACTOR=0.001)


if __name__ == '__main__':
    unittest.main()
