import unittest

from reamber.osu.OsuMap import OsuMap
from reamber.algorithms.playField import PlayField
from reamber.algorithms.playField.parts import *

from tests.test.RSC_PATHS import OSU_BOOGIE

from reamber.algorithms.pattern.Pattern import Pattern
from reamber.algorithms.pattern.combos.PtnCombo import PtnCombo


class TestImagePattern(unittest.TestCase):

    def test_osu(self):
        osu = OsuMap.read_file(OSU_BOOGIE)

        ptn = Pattern.from_note_lists([osu.notes.hits(), osu.notes.holds()])
        grp = ptn.group(h_window=None, v_window=50, avoid_jack=True)

        keys = osu.notes.max_column() + 1

        pf = PlayField(m=osu, duration_per_px=5) \
             + PFDrawLines.from_combo(keys=keys, **PFDrawLines.Colors.RED,
                                      combo=PtnCombo(grp).template_chord_stream(primary=3, secondary=2, keys=keys, and_lower=True)) \
             + PFDrawLines.from_combo(keys=keys, **PFDrawLines.Colors.BLUE,
                                      combo=PtnCombo(grp).template_chord_stream(primary=2, secondary=1, keys=keys, and_lower=True)) \
             + PFDrawLines.from_combo(keys=keys, **PFDrawLines.Colors.PURPLE,
                                      combo=PtnCombo(grp).template_jacks(minimum_length=2, keys=keys))

        # pf.exportFold(maxHeight=1750, stageLineWidth=0).save("osu.png")

        pass

if __name__ == '__main__':
    unittest.main()
