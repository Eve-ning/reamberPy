import unittest

from reamber.algorithms.convert.SMToQua import SMToQua
from reamber.sm.SMMapSet import SMMapSet
from tests.test.RSC_PATHS import *


# import logging
#
# logging.basicConfig(filename="event.log", filemode="w+", level=logging.DEBUG)


class TestSMToQua(unittest.TestCase):

    # @profile
    def test(self):
        # Complex BPM Points

        sm = SMMapSet.readFile(SM_GRAVITY)

        quas = SMToQua.convert(sm)
        quas[0].writeFile("gravity.qua")

    def test2(self):
        # Stops and multiple map

        sm = SMMapSet.readFile(SM_ESCAPES)

        quas = SMToQua.convert(sm)
        quas[0].writeFile("escapes1.qua")
        quas[1].writeFile("escapes2.qua")


if __name__ == '__main__':
    unittest.main()
