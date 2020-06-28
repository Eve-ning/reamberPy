import unittest

from reamber.algorithms.convert.QuaToOsu import QuaToOsu
from reamber.quaver.QuaMap import QuaMap
from tests.test.RSC_PATHS import *


# import logging
#
# logging.basicConfig(filename="event.log", filemode="w+", level=logging.DEBUG)


class TestQuaToOsu(unittest.TestCase):

    # @profile
    def test_qua1(self):
        # Complex BPM Points
        qua = QuaMap()
        qua.readFile(QUA_NEURO_CLOUD)

        osu = QuaToOsu.convert(qua)
        osu.writeFile("out.osu")


if __name__ == '__main__':
    unittest.main()
