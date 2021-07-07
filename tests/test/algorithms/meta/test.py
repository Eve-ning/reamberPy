import logging
import unittest

from reamber.algorithms.mutate.hitSoundCopy import hitsound_copy
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
        m_from = OsuMap.read_file(OSU_TRIBAL_TRIAL_MX)

        m_to = OsuMap.read_file(OSU_TRIBAL_TRIAL_EXH)

        m_out = hitsound_copy(m_from=m_from, m_to=m_to)

        # m_out.writeFile("out.osu")

        m_out = hitsound_copy(m_from=m_out, m_to=m_from)

        # m_out.writeFile("out.osu")


if __name__ == '__main__':
    unittest.main()
