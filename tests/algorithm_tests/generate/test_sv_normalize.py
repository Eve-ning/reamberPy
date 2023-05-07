import pytest

from reamber.algorithms.generate import sv_normalize
from reamber.osu import OsuMap, OsuBpm
from reamber.osu.lists import OsuBpmList


@pytest.fixture(scope='module')
def osu_map() -> OsuMap:
    """ Tests our scroll speed analysis algorithm

        Test Scenario

        OFFSET |  0  | 100 | 200 | 300
        -------------------------------
        BPMS   | 100 |     | 200 | 400
        -------------------------------
        SPEED  |  1  |  2  |  2  |  3
        NORM   |  1  |  1  | 0.5 | 0.25

        """

    osu_map = OsuMap()
    osu_map.bpms = OsuBpmList([OsuBpm(0, 100, 4, volume=100),
                               OsuBpm(200, 200, 4, volume=50),
                               OsuBpm(300, 400, 4, volume=0), ])
    return osu_map


def test_sv_normalize(osu_map: OsuMap):
    svs = sv_normalize(osu_map)
    # Test that the normalize multiplier is right
    assert all(svs.multiplier == [1, 0.5, 0.25])
    # Test that bpm attributes are propagated correctly
    assert all(svs.volume == [100, 50, 0])


def test_sv_normalize_override(osu_map: OsuMap):
    svs = sv_normalize(osu_map, override_bpm=200)
    # Test that the normalize multiplier is right
    assert all(svs.multiplier == [2, 1, 0.5])
    # Test that bpm attributes are propagated correctly
    assert all(svs.volume == [100, 50, 0])
