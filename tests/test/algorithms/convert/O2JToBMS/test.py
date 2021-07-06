import unittest

from reamber.algorithms.convert.O2JToBMS import O2JToBMS
from reamber.o2jam.O2JMapSet import O2JMapSet
from tests.test.RSC_PATHS import *
from reamber.bms.BMSChannel import BMSChannel


# import logging
#
# logging.basicConfig(filename="event.log", filemode="w+", level=logging.DEBUG)


class TestO2JToBMS(unittest.TestCase):

    # @profile
    def test(self):
        # Complex BPM Points
        o2j = O2JMapSet.readFile(O2J_FLY_MAGPIE_OJN)

        bms = O2JToBMS.convert(o2j)
        bms[1].write_file('out.bme', BMSChannel.BME)


if __name__ == '__main__':
    unittest.main()
