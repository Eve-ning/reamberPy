import numpy as np
import pytest

from reamber.algorithms.pattern.Pattern import Pattern
from reamber.algorithms.pattern.combos.PtnCombo import PtnCombo
from reamber.algorithms.playField import PlayField
from reamber.algorithms.playField.parts import *
from reamber.base.Map import Map
from reamber.osu.OsuMap import OsuMap
from reamber.quaver.QuaMap import QuaMap
from tests.conftest import MAPS_DIR


@pytest.mark.parametrize(
    'map_str',
    ['osu_map', 'qua_map', 'sm_map', 'o2j_map', 'bms_map']
)
def test_draw(map_str: str, request):
    map: Map = request.getfixturevalue(map_str)
    ptn = Pattern.from_note_lists([map.hits, map.holds], include_tails=False)
    grp = ptn.group()

    keys = map.stack().column.max() + 1

    pf = (
        PlayField(m=map, duration_per_px=5, padding=40) +
        PFDrawBpm() +
        PFDrawBeatLines() +
        PFDrawColumnLines() +
        PFDrawNotes() +
        PFDrawOffsets() +
        PFDrawLines.from_combo(
            **PFDrawLines.Colors.RED, furthest=1000,
            keys=keys,
            combo=np.concatenate(PtnCombo(grp).template_chord_stream(
                primary=3, secondary=2,
                keys=keys, and_lower=True
            ), axis=0)
        ) +
        PFDrawLines.from_combo(
            **PFDrawLines.Colors.PURPLE,
            keys=keys,
            combo=np.concatenate(PtnCombo(grp).template_jacks(
                minimum_length=2, keys=keys), axis=0)
        )
    )

    pf.export_fold(max_height=1000) # .save(f"{map_str}.png")

@pytest.mark.parametrize(
    'map_str, map_path, GameMap',
    [("osu_sv", MAPS_DIR / 'osu/BackBeat.osu', OsuMap),
     ("qua_sv", MAPS_DIR / 'qua/CarryMeAway.qua', QuaMap)]
)
def test_draw_sv(map_str, map_path, GameMap: Map):
    map = GameMap.read_file(map_path)
    ptn = Pattern.from_note_lists([map.hits, map.holds], include_tails=False)
    grp = ptn.group()

    keys = map.stack().column.max() + 1

    pf = (
        PlayField(m=map, duration_per_px=5, padding=30) +
        PFDrawBpm() +
        PFDrawSv() +
        PFDrawBeatLines() +
        PFDrawColumnLines() +
        PFDrawNotes() +
        PFDrawLines.from_combo(
            **PFDrawLines.Colors.RED, furthest=1000,
            keys=keys,
            combo=np.concatenate(PtnCombo(grp).template_chord_stream(
                primary=3, secondary=2,
                keys=keys, and_lower=True
            ), axis=0)
        ) +
        PFDrawLines.from_combo(
            **PFDrawLines.Colors.PURPLE,
            keys=keys,
            combo=np.concatenate(PtnCombo(grp).template_jacks(
                minimum_length=2, keys=keys), axis=0)
        )
    )

    pf.export_fold(max_height=2500) # .save(f"{map_str}.png")
