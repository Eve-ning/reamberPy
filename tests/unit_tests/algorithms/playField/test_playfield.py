import numpy as np
import pytest

from reamber.algorithms.pattern.Pattern import Pattern
from reamber.algorithms.pattern.combos.PtnCombo import PtnCombo
from reamber.algorithms.playField import PlayField
from reamber.algorithms.playField.parts import *
from reamber.base.Map import Map


@pytest.mark.parametrize(
    'map',
    ['osu_map']  # , 'qua_map', 'sm_map', 'o2j_map', 'bms_map']
)
def test_draw_from_combo(map_str: str, request):
    map: Map = request.getfixturevalue(map_str)
    ptn = Pattern.from_note_lists([map.hits, map.holds])
    grp = ptn.group(h_window=None, v_window=50, avoid_jack=True)

    keys = map.stack().column.max() + 1

    pf = (
        PlayField(m=map, duration_per_px=5) +
        PFDrawLines.from_combo(
            **PFDrawLines.Colors.RED,
            keys=keys,
            combo=np.concatenate(PtnCombo(grp).template_chord_stream(
                primary=3, secondary=2,
                keys=keys, and_lower=True), axis=0)
        ) +
        PFDrawLines.from_combo(
            **PFDrawLines.Colors.PURPLE,
            keys=keys,
            combo=np.concatenate(PtnCombo(grp).template_jacks(
                minimum_length=2, keys=keys), axis=0)
        ) +
        PFDrawNotes() +
        PFDrawBpm() +
        PFDrawBeatLines() +
        PFDrawColumnLines()
    )

    pf.export_fold(max_height=1000)
