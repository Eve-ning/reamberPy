import unittest
from tests.test.RSC_PATHS import *

from reamber.o2jam.O2JMapSetObj import O2JMapSetObj
from reamber.osu.OsuMapObj import OsuMapObj
from reamber.quaver.QuaMapObj import QuaMapObj
from reamber.sm.SMMapSetObj import SMMapSetObj
from reamber.algorithms.analysis.image import image

class TestImage(unittest.TestCase):

    def test_osu(self):
        from reamber.osu.OsuMapObj import OsuMapObj
        m = OsuMapObj()
        m.readFile("../../../../../" + OSU_JOUNETSU)
        image(m, noteWidth=10, beatLines=[1, 2, 4]).save("osu.png")

    def test_qua(self):
        m = QuaMapObj()
        m.readFile("../../../../../" + QUA_NEURO_CLOUD)
        image(m, noteWidth=10, beatLines=[1, 2, 4]).save("qua.png")

    def test_sm(self):
        s = SMMapSetObj()
        s.readFile("../../../../../" + SM_CARAVAN)
        image(s.maps[0], noteWidth=10, beatLines=[1, 2, 4]).save("sm.png")

    def test_o2j(self):
        s = O2JMapSetObj()
        s.readFile("../../../../../" + O2J_FLY_MAGPIE_OJN)
        image(s.maps[0], noteWidth=10, beatLines=[1, 2, 4]).save("o2j.png")


if __name__ == '__main__':
    unittest.main()
