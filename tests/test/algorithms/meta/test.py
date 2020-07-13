import logging
import unittest

from reamber.algorithms.mutate.hitSoundCopy import hitSoundCopy
from reamber.osu.OsuMap import OsuMap
from tests.test.RSC_PATHS import *

logging.basicConfig(filename="event.log", filemode="w+", level=logging.DEBUG)


class TestHitsoundCopy(unittest.TestCase):

    # # @profile
    # def test_osu1(self):
    #     mFrom = OsuMap()
    #     mFrom.readFile(OSU_AVENGER_HITSOUNDFILE)
    #
    #     mTo = OsuMap()
    #     mTo.readFile(OSU_AVENGER_HITSOUNDABLE)
    #
    #     mOut = hitSoundCopy(mFrom=mFrom, mTo=mTo)
    #
    #     mOut.writeFile("out.osu")

    # @profile
    def test_osu2(self):
        mFrom = OsuMap.readFile(OSU_TRIBAL_TRIAL_MX)

        mTo = OsuMap.readFile(OSU_TRIBAL_TRIAL_EXH)

        mOut = hitSoundCopy(mFrom=mFrom, mTo=mTo)

        mOut.writeFile("out.osu")

        mOut = hitSoundCopy(mFrom=mOut, mTo=mFrom)

        mOut.writeFile("out.osu")


if __name__ == '__main__':
    unittest.main()
