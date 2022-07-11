from pathlib import Path

import pytest

from reamber.sm.SMMapSet import SMMapSet
from tests.conftest import MAPS_DIR

MAP_PATH = MAPS_DIR / "sm/Caravan.sm"


@pytest.fixture(scope='module')
def sm_mapset() -> SMMapSet:
    return SMMapSet.read_file(MAP_PATH)


def test_write(sm_mapset):
    with open(Path(__file__).parent / "gt_caravan.sm", "r") as f:
        h = hash(f.read())
    assert h == hash(sm_mapset.write())


def test_first_hit(sm_mapset):
    assert sm_mapset[0].hits.first_offset() == \
           pytest.approx(696, abs=1)


def test_last_hit(sm_mapset):
    assert sm_mapset[0].hits.last_offset() == \
           pytest.approx(9 * 60000 + 8167, abs=2)


def test_first_hold(sm_mapset):
    assert sm_mapset[0].holds.first_offset() == \
           pytest.approx(375, abs=1)


def test_last_hold(sm_mapset):
    assert sm_mapset[0].holds.last_offset() == \
           pytest.approx(9 * 60000 + 8736, abs=2)


def test_hit_count(sm_mapset):
    assert len(sm_mapset[0].hits) == 4919
    assert len(sm_mapset[0].holds) == 1358
