import unittest

from reamber.algorithms.convert.BMSToSM import BMSToSM
from reamber.bms.BMSMap import BMSMap
from reamber.bms.BMSChannel import BMSChannel
from tests.test.RSC_PATHS import *

# import logging
#
# logging.basicConfig(filename="event.log", filemode="w+", level=logging.DEBUG)


class TestBMSToSM(unittest.TestCase):

    # @profile
    def test(self):
        # Complex BPM Points
        bms = BMSMap.read_file(BMS_SAMBALAND, BMSChannel.BME)

        sm = BMSToSM.convert(bms)
        # sm.writeFile("out.sm")


if __name__ == '__main__':
    unittest.main()
