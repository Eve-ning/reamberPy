import unittest

from reamber.algorithms.convert.SMToOsu import SMToOsu
from reamber.sm.SMMapSet import SMMapSet
from tests.test.RSC_PATHS import *


# import logging
#
# logging.basicConfig(filename="event.log", filemode="w+", level=logging.DEBUG)


class TestSMToOsu(unittest.TestCase):

    # @profile
    def test_sm1(self):
        # Complex BPM Points

        sm = SMMapSet.readFile(SM_GRAVITY)

        osuMapSet = SMToOsu.convert(sm)
        osuMapSet[0].audioFileName = "audio.mp3"
        osuMapSet[0].addOffset(15 + 41)
        # osuMapSet[0].writeFile("out.osu")

    def test_sm2(self):
        # Stops and multiple map

        sm = SMMapSet.readFile(SM_ESCAPES)

        osuMapSet = SMToOsu.convert(sm)
        osuMapSet[0].audioFileName = "Escapes.mp3"
        osuMapSet[0].addOffset(635 + 575)
        # osuMapSet[0].writeFile("out.osu")

        osuMapSet[1].audioFileName = "Escapes.mp3"
        osuMapSet[1].addOffset(635 + 575)
        # osuMapSet[1].writeFile("out.osu")


if __name__ == '__main__':
    unittest.main()
