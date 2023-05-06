import pytest

from reamber.algorithms.analysis import scroll_speed
from reamber.osu import OsuBpm, OsuSv, OsuHit
from reamber.osu.OsuMap import OsuMap
from reamber.osu.lists import OsuBpmList, OsuSvList
from reamber.osu.lists.notes import OsuHitList
from reamber.sm import SMMap, SMBpm, SMHit
from reamber.sm.lists import SMBpmList
from reamber.sm.lists.notes import SMHitList


@pytest.fixture(scope='module')
def osu_map():
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
    osu_map.bpms = OsuBpmList([OsuBpm(0, 100, 4), OsuBpm(200, 200, 4), OsuBpm(300, 300, 4), ])
    osu_map.svs = OsuSvList([OsuSv(0, 1, 4), OsuSv(100, 2, 4), OsuSv(200, 1, 4)])
    osu_map.hits = OsuHitList([OsuHit(-100, 0), OsuHit(400, 0), ])
    return osu_map


@pytest.fixture(scope='module')
def sm_map():
    """ Tests our scroll speed analysis algorithm

       Test Scenario

       OFFSET | -100|  0  | 200 | 300 | 400 |
       ---------------------------------------
       HITS   |  x  |     |     |     |  x  |
       BPMS   |     | 100 | 200 | 300 |     |
       ---------------------------------------
       SPEED  |  1  |  1  |  2  |  3  |  3  |

       """

    sm_map = SMMap()
    sm_map.bpms = SMBpmList([SMBpm(0, 100, 4), SMBpm(200, 200, 4), SMBpm(300, 300, 4), ])
    sm_map.hits = SMHitList([SMHit(-100, 0), SMHit(400, 0), ])
    return sm_map


def test_scroll_speed_sv(osu_map):
    assert all(scroll_speed(osu_map) == [1, 1, 2, 2, 3, 3])

def test_scroll_speed_sv_override(osu_map):
    assert all(scroll_speed(osu_map, 50) == [2, 2, 4, 4, 6, 6])


def test_scroll_speed_nosv(sm_map):
    assert all(scroll_speed(sm_map) == [1, 1, 2, 3, 3])


def test_scroll_speed_nosv_override(sm_map):
    assert all(scroll_speed(sm_map, 50) == [2, 2, 4, 6, 6])

