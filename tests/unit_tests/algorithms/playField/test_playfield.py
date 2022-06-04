import pytest

from reamber.algorithms.pattern.Pattern import Pattern
from reamber.algorithms.pattern.combos.PtnCombo import PtnCombo
from reamber.algorithms.playField import PlayField
from reamber.algorithms.playField.parts import *


@pytest.mark.parametrize(
    'map',
    ['osu_map', 'qua_map', 'sm_map', 'o2j_map', 'bms_map']
)
def test_osu(map, request):
    map = request.getfixturevalue(map)
    ptn = Pattern.from_note_lists([
        map.notes.hits(),
        map.notes.holds()
    ])
    grp = ptn.group(h_window=None, v_window=50, avoid_jack=True)

    keys = map.notes.max_column() + 1

    pf = (
        PlayField(m=map, duration_per_px=5)
        + PFDrawLines.from_combo(**PFDrawLines.Colors.RED,
                                 keys=keys,
                                 combo=PtnCombo(grp).template_chord_stream(
                                     primary=3, secondary=2,
                                     keys=keys, and_lower=True)
                                 )
        + PFDrawLines.from_combo(**PFDrawLines.Colors.BLUE,
                                 keys=keys,
                                 combo=PtnCombo(grp).template_chord_stream(
                                     primary=2, secondary=1,
                                     keys=keys, and_lower=True)
                                 )
        + PFDrawLines.from_combo(**PFDrawLines.Colors.PURPLE,
                                 keys=keys,
                                 combo=PtnCombo(grp).template_jacks(
                                     minimum_length=2, keys=keys))
    )
