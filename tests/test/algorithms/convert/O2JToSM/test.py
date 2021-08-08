import unittest

from reamber.algorithms.convert.O2JToSM import O2JToSM
from reamber.o2jam.O2JMapSet import O2JMapSet
from tests.test.RSC_PATHS import *


# import logging
#
# logging.basicConfig(filename="event.log", filemode="w+", level=logging.DEBUG)


class TestOsuToQua(unittest.TestCase):

    # @profile
    def test(self):
        # Complex BPM Points
        o2j = O2JMapSet.read_file(O2J_FLY_MAGPIE_OJN)

        sms = O2JToSM.convert(o2j)
        # sms[0].writeFile("out.sm")
        # sms[1].writeFile("out.sm")
        # sms[2].writeFile("out.sm")


if __name__ == '__main__':
    unittest.main()
