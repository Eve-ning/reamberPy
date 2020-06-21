import unittest
from tests.test.RSC_PATHS import *

from reamber.algorithms.convert.O2JToSM import O2JToSM
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

        sms = O2JToSM.convert(o2j)
        sms[0].writeFile("flymagpie0.sm")
        sms[1].writeFile("flymagpie1.sm")
        sms[2].writeFile("flymagpie2.sm")

    # @profile
    def test_o2j2(self):
        # Complex BPM Points
        o2j = O2JMapSetObj()
        o2j.readFile(O2J_CHECK_IT_OUT_OJN)

        sms = O2JToSM.convert(o2j)
        sms[0].writeFile("checkitout0.sm")
        sms[1].writeFile("checkitout1.sm")
        sms[2].writeFile("checkitout2.sm")


if __name__ == '__main__':
    unittest.main()
