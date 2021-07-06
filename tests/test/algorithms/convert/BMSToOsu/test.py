import unittest

from reamber.algorithms.convert.BMSToOsu import BMSToOsu
from reamber.bms.BMSMap import BMSMap
from reamber.bms.BMSChannel import BMSChannel
from tests.test.RSC_PATHS import *

# import logging
#
# logging.basicConfig(filename="event.log", filemode="w+", level=logging.DEBUG)


class TestBMSToOsu(unittest.TestCase):

    # @profile
    def test(self):
        # Complex BPM Points
        bms = BMSMap.read_file(BMS_SAMBALAND, BMSChannel.BME)

        osu = BMSToOsu.convert(bms)
        # osu.writeFile("out.osu")


if __name__ == '__main__':
    unittest.main()
