import unittest
from tests.test.RSC_PATHS import *

from reamber.algorithms.convert.O2JToOsu import O2JToOsu
from reamber.o2jam.O2JMapSetObj import O2JMapSetObj
# import logging
#
# logging.basicConfig(filename="event.log", filemode="w+", level=logging.DEBUG)


class TestOsuToQua(unittest.TestCase):

    # @profile
    def test_o2j1(self):
        # Complex BPM Points
        o2j = O2JMapSetObj()
        o2j.readFile(O2J_FLY_MAGPIE_OJN)

        osus = O2JToOsu.convert(o2j)
        osus[0].writeFile("flymagpie0.osu")
        osus[1].writeFile("flymagpie1.osu")
        osus[2].writeFile("flymagpie2.osu")

    # @profile
    def test_o2j2(self):
        # Complex BPM Points
        o2j = O2JMapSetObj()
        o2j.readFile(O2J_CHECK_IT_OUT_OJN)

        osus = O2JToOsu.convert(o2j)
        osus[0].writeFile("checkitout0.osu")
        osus[1].writeFile("checkitout1.osu")
        osus[2].writeFile("checkitout2.osu")


if __name__ == '__main__':
    unittest.main()
