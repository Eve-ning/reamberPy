import unittest

from reamber.algorithms.convert.BMSToQua import BMSToQua
from reamber.bms.BMSMap import BMSMap
from reamber.bms.BMSChannel import BMSChannel
from tests.test.RSC_PATHS import *

# import logging
#
# logging.basicConfig(filename="event.log", filemode="w+", level=logging.DEBUG)


class TestBMSToQua(unittest.TestCase):

    # @profile
    def test(self):
        # Complex BPM Points
        bms = BMSMap.readFile(BMS_SAMBALAND, BMSChannel.BME)

        qua = BMSToQua.convert(bms)
        # qua.writeFile("out.qua")



if __name__ == '__main__':
    unittest.main()
