import unittest

from reamber.algorithms.convert.OsuToBMS import OsuToBMS
from reamber.osu.OsuMap import OsuMap
from tests.test.RSC_PATHS import *
from reamber.bms.BMSChannel import BMSChannel


# import logging
#
# logging.basicConfig(filename="event.log", filemode="w+", level=logging.DEBUG)


class TestOsuToBMS(unittest.TestCase):

    # @profile
    def test(self):
        # Complex BPM Points
        osu = OsuMap.read_file(OSU_ZENITHALIZE_19)

        bms = OsuToBMS.convert(osu, moveRightBy=1)
        bms.write_file('out.bme', BMSChannel.BME)


if __name__ == '__main__':
    unittest.main()
