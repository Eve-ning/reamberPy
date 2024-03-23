from reamber.algorithms.utils import dominant_bpm
from reamber.osu import OsuMap, OsuBpm, OsuHit
from reamber.osu.lists import OsuBpmList
from reamber.osu.lists.notes import OsuHitList


def test_dominant_bpm():
    """Tests our scroll speed analysis algorithm

    Test Scenario

    OFFSET | -100|  0  | 100 | 200 | 300 | 600 |
    ---------------------------------------------
    HITS   |  x  |     |     |     |     |  x  |
    BPMS   |     | 100 |     | 200 | 300 |     |
    Activ  |     | <-------> | <-> | <-------> |
    """

    osu_map = OsuMap()
    osu_map.bpms = OsuBpmList(
        [
            OsuBpm(0, 100, 4),
            OsuBpm(200, 200, 4),
            OsuBpm(300, 300, 4),
        ]
    )
    osu_map.hits = OsuHitList(
        [
            OsuHit(-100, 0),
            OsuHit(600, 0),
        ]
    )
    assert dominant_bpm(osu_map) == 300
