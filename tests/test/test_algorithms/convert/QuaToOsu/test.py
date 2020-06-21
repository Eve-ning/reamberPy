import unittest
from tests.test.RSC_PATHS import *

from reamber.algorithms.convert.QuaToOsu import QuaToOsu
from reamber.quaver.QuaMapObj import QuaMapObj
# import logging
#
# logging.basicConfig(filename="event.log", filemode="w+", level=logging.DEBUG)


class TestQuaToOsu(unittest.TestCase):

    # @profile
    def test_qua1(self):
        # Complex BPM Points
        qua = QuaMapObj()
        qua.readFile(QUA_NEURO_CLOUD)

        osu = QuaToOsu.convert(qua)
        osu.writeFile("neurocloud.osu")


if __name__ == '__main__':
    unittest.main()
