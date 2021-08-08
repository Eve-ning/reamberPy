import unittest

from reamber.algorithms.convert.O2JToQua import O2JToQua
from reamber.o2jam.O2JMapSet import O2JMapSet
from tests.test.RSC_PATHS import *


# import logging
#
# logging.basicConfig(filename="event.log", filemode="w+", level=logging.DEBUG)


class TestO2JToQua(unittest.TestCase):

    # @profile
    def test(self):
        # Complex BPM Points
        o2j = O2JMapSet.read_file(O2J_FLY_MAGPIE_OJN)

        quas = O2JToQua.convert(o2j)
        # quas[0].writeFile("out.qua")
        # quas[1].writeFile("out.qua")
        # quas[2].writeFile("out.qua")


if __name__ == '__main__':
    unittest.main()
