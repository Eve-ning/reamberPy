import unittest

from reamber.algorithms.convert.SMToBMS import SMToBMS
from reamber.sm.SMMapSet import SMMapSet
from tests.test.RSC_PATHS import *
from reamber.bms.BMSChannel import BMSChannel


# import logging
#
# logging.basicConfig(filename="event.log", filemode="w+", level=logging.DEBUG)


class TestSMToBMS(unittest.TestCase):

    # @profile
    def test(self):
        # This is not going to give me a proper map but ok
        sm = SMMapSet.readFile(SM_ICFITU)

        bms = SMToBMS.convert(sm)
        bms[0].write_file('out.bme', BMSChannel.BME)


if __name__ == '__main__':
    unittest.main()
