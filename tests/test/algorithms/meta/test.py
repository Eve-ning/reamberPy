import unittest
from tests.test.RSC_PATHS import *

from reamber.osu.OsuMapObj import OsuMapObj
from reamber.algorithms.meta.hitSoundCopy import hitSoundCopy

import logging

logging.basicConfig(filename="event.log", filemode="w+", level=logging.DEBUG)


class TestHitsoundCopy(unittest.TestCase):

    # @profile
    def test_osu1(self):
        mFrom = OsuMapObj()
        mFrom.readFile("../../../../" + OSU_AVENGER_HITSOUNDFILE)

        mTo = OsuMapObj()
        mTo.readFile("../../../../" + OSU_AVENGER_HITSOUNDABLE)

        mOut = hitSoundCopy(mFrom=mFrom, mTo=mTo)
        
        mOut.writeFile("avenger.osu")

    # @profile
    def test_osu2(self):
        """ The purpose of this test is for upcasting, where there may be too """

        mFrom = OsuMapObj()
        mFrom.readFile("../../../../" + OSU_TRIBAL_TRIAL_MX)

        mTo = OsuMapObj()
        mTo.readFile("../../../../" + OSU_TRIBAL_TRIAL_EXH)

        mOut = hitSoundCopy(mFrom=mFrom, mTo=mTo)

        mOut.writeFile("tribalTrialEXH.osu")

        mOut = hitSoundCopy(mFrom=mOut, mTo=mFrom)

        mOut.writeFile("tribalTrialMX.osu")


if __name__ == '__main__':
    unittest.main()