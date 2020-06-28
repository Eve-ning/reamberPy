import unittest

from reamber.algorithms.convert.SMToQua import SMToQua
from reamber.sm.SMMapSet import SMMapSet
from tests.test.RSC_PATHS import *


# import logging
#
# logging.basicConfig(filename="event.log", filemode="w+", level=logging.DEBUG)


class TestSMToQua(unittest.TestCase):

    # @profile
    def test_sm1(self):
        # Complex BPM Points

        sm = SMMapSet()
        sm.readFile(SM_GRAVITY)

        quaMapSet = SMToQua.convert(sm)
        quaMapSet[0].writeFile("out.qua")

    def test_sm2(self):
        # Stops and multiple map

        sm = SMMapSet()
        sm.readFile(SM_ESCAPES)

        quaMapSet = SMToQua.convert(sm)
        quaMapSet[0].writeFile("out.qua")
        quaMapSet[1].writeFile("out.qua")


if __name__ == '__main__':
    unittest.main()
