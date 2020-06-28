import unittest
from tests.test.RSC_PATHS import *

from reamber.algorithms.convert.QuaToSM import QuaToSM
from reamber.quaver.QuaMapObj import QuaMapObj
# import logging
#
# logging.basicConfig(filename="event.log", filemode="w+", level=logging.DEBUG)


class TestQuaToSm(unittest.TestCase):

    # @profile
    def test_qua1(self):
        # Complex BPM Points
        qua = QuaMapObj()
        qua.readFile(QUA_NEURO_CLOUD)

        sm = QuaToSM.convert(qua)
        sm.writeFile("out.sm")


if __name__ == '__main__':
    unittest.main()
