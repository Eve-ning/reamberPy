import unittest

from reamber.algorithms.convert.SMToOsu import SMToOsu
from reamber.sm.SMMapSet import SMMapSet
from tests.test.RSC_PATHS import *


# import logging
#
# logging.basicConfig(filename="event.log", filemode="w+", level=logging.DEBUG)


class TestSMToOsu(unittest.TestCase):

    # @profile
    def test(self):
        # Complex BPM Points

        sm = SMMapSet.read_file(SM_GRAVITY)

        osuMapSet = SMToOsu.convert(sm)
        osuMapSet[0].audio_file_name = "audio.mp3"
        osuMapSet[0].offset += 15 + 41
        # osuMapSet[0].writeFile("out.osu")

    def test2(self):
        # Stops and multiple map

        sm = SMMapSet.read_file(SM_ESCAPES)

        osuMapSet = SMToOsu.convert(sm)
        osuMapSet[0].audio_file_name = "Escapes.mp3"
        osuMapSet[0].offset += 635 + 575
        # osuMapSet[0].writeFile("out.osu")

        osuMapSet[1].audio_file_name = "Escapes.mp3"
        osuMapSet[1].offset += 635 + 575
        # osuMapSet[1].writeFile("out.osu")


if __name__ == '__main__':
    unittest.main()
