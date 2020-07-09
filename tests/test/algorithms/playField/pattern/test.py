import unittest

from reamber.osu.OsuMap import OsuMap
from reamber.algorithms.playField import PlayField
from reamber.algorithms.playField.parts import *

from tests.test.RSC_PATHS import OSU_BOOGIE

from reamber.algorithms.pattern.Pattern import Pattern

class TestImagePattern(unittest.TestCase):

    def test_osu(self):

        osu = OsuMap()
        osu.readFile(OSU_BOOGIE)

        ptn = Pattern.fromPkg([osu.notes.hits(), osu.notes.holds()])
        grp = ptn.group(hwindow=None, vwindow=50, avoidJack=True)

        keys = osu.notes.maxColumn() + 1

        pf = PlayField(m=osu, durationPerPx=5) \
             + PFDrawLines.templateChordStream(primary=3,
                                               secondary=2,
                                               keys=keys,
                                               groups=grp,
                                               **PFDrawLines.Colors.BLUE, fromWidth=3) \
             + PFDrawLines.templateChordStream(primary=2,
                                               secondary=1,
                                               keys=keys,
                                               groups=grp,
                                               **PFDrawLines.Colors.PURPLE, fromWidth=3) \
             + PFDrawLines.templateJacks(minimumLength=2,
                                         keys=keys,
                                         groups=grp,
                                         **PFDrawLines.Colors.RED, fromWidth=2)
        pf.exportFold(maxHeight=1750, stageLineWidth=0).save("osu.png")

        pass

if __name__ == '__main__':
    unittest.main()
