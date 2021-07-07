import unittest

from reamber.algorithms.convert.QuaToOsu import QuaToOsu
from reamber.quaver.QuaMap import QuaMap
from tests.test.RSC_PATHS import *


# import logging
#
# logging.basicConfig(filename="event.log", filemode="w+", level=logging.DEBUG)


class TestQuaToOsu(unittest.TestCase):

    # @profile
    def test(self):
        # Complex BPM Points
        qua = QuaMap.read_file(QUA_NEURO_CLOUD)

        osu = QuaToOsu.convert(qua)
        # osu.writeFile("out.osu")


if __name__ == '__main__':
    unittest.main()
