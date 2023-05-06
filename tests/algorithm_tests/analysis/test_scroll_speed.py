from reamber.algorithms.analysis import scroll_speed
from reamber.osu import OsuBpm, OsuSv, OsuHit
from reamber.osu.OsuMap import OsuMap
from reamber.osu.lists import OsuBpmList, OsuSvList
from reamber.osu.lists.notes import OsuHitList


def test_scroll_speed():
    """ Tests our scroll speed analysis algorithm

    Test Scenario

    OFFSET | -100|  0  | 100 | 200 | 300 | 400 |
    ---------------------------------------------
    HITS   |  x  |     |     |     |     |  x  |
    BPMS   |     | 100 |     | 200 | 300 |     |
    SVS    |     |  1  |  2  |  1  |     |     |
    ---------------------------------------------
    SPEED  |  1  |  1  |  2  |  2  |  3  |  3  |

    """

    osu_map = OsuMap()
    osu_map.bpms = OsuBpmList([
        OsuBpm(0, 100, 4),
        OsuBpm(200, 200, 4),
        OsuBpm(300, 300, 4),
    ])
    osu_map.svs = OsuSvList([
        OsuSv(0, 1, 4),
        OsuSv(100, 2, 4),
        OsuSv(200, 1, 4)
    ])
    osu_map.hits = OsuHitList([
        OsuHit(-100, 0),
        OsuHit(400, 0),
    ])
    assert all(scroll_speed(osu_map) == [1, 1, 2, 2, 3, 3])
