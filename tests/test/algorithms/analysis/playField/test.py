import unittest
from tests.test.RSC_PATHS import *

from reamber.o2jam.O2JMapSetObj import O2JMapSetObj
from reamber.osu.OsuMapObj import OsuMapObj
from reamber.quaver.QuaMapObj import QuaMapObj
from reamber.sm.SMMapSetObj import SMMapSetObj
from reamber.algorithms.analysis.playField import PlayField
from reamber.algorithms.analysis.playField.parts import *

class TestImage(unittest.TestCase):

    def test_osu(self):
        m = OsuMapObj()
        m.readFile(OSU_CARAVAN)
        pf = PlayField(m, padding=70)\
             + PFDrawColumnLines()\
             + PFDrawBeatLines()\
             + PFDrawBpm(xOffset=30, yOffset=0)\
             + PFDrawSv(yOffset=0)\
             + PFDrawNotes()
        pf.exportFold(maxHeight=1000).save("osu.png")

    def test_qua(self):
        m = QuaMapObj()
        m.readFile(QUA_NEURO_CLOUD)
        pf = PlayField(m)\
             + PFDrawColumnLines()\
             + PFDrawBeatLines([1,3,6])\
             + PFDrawNotes()
        pf.exportFold(maxHeight=2000).save("qua.png")

    def test_sm(self):
        s = SMMapSetObj()
        s.readFile(SM_ICFITU)
        pf = PlayField(s.maps[0])\
             + PFDrawBeatLines([1])\
             + PFDrawNotes()
        pf.exportFold(maxHeight=2000).save("sm.png")

    def test_o2j(self):
        s = O2JMapSetObj()
        s.readFile(O2J_FLY_MAGPIE_OJN)
        pf = PlayField(s.maps[2], padding=40)\
             + PFDrawColumnLines()\
             + PFDrawBeatLines([1])\
             + PFDrawBpm()\
             + PFDrawNotes()
        pf.exportFold(maxHeight=2000).save("o2j.png")


if __name__ == '__main__':
    unittest.main()
