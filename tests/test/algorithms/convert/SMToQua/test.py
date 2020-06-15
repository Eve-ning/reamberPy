import unittest
from tests.test.RSC_PATHS import *

from reamber.algorithms.convert.SMToQua import SMToQua
from reamber.sm.SMMapSetObj import SMMapSetObj

# import logging
#
# logging.basicConfig(filename="event.log", filemode="w+", level=logging.DEBUG)


class TestSMToQua(unittest.TestCase):

    # @profile
    def test_sm1(self):
        # Complex BPM Points

        sm = SMMapSetObj()
        sm.readFile("../../../../../" + SM_GRAVITY)

        quaMapSet = SMToQua.convert(sm)
        quaMapSet[0].writeFile("gravity.qua")

    def test_sm2(self):
        # Stops and multiple map

        sm = SMMapSetObj()
        sm.readFile("../../../../../" + SM_ESCAPES)

        quaMapSet = SMToQua.convert(sm)
        quaMapSet[0].writeFile("escapes1.qua")
        quaMapSet[1].writeFile("escapes2.qua")


if __name__ == '__main__':
    unittest.main()