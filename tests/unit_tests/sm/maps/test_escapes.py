from pathlib import Path

import pytest

from reamber.sm.SMMapSet import SMMapSet
from tests.conftest import MAPS_DIR

MAP_PATH = MAPS_DIR / "sm/Escapes.sm"


@pytest.fixture(scope='module')
def sm_mapset() -> SMMapSet:
    return SMMapSet.read_file(MAP_PATH)


def test_write(sm_mapset):
    with open(Path(__file__).parent /"gt_escapes.sm", "r") as f:
        h = hash(f.read())
    assert h == hash(sm_mapset.write())


def test_first_hit(sm_mapset):
    assert sm_mapset[0].hits.first_offset() == \
           pytest.approx(635, abs=1)


def test_last_hit(sm_mapset):
    assert sm_mapset[0].hits.last_offset() == \
           pytest.approx(2 * 60000 + 42921, abs=2)


def test_first_hold(sm_mapset):
    assert sm_mapset[0].holds.first_offset() == \
           pytest.approx(635, abs=1)


def test_last_hold(sm_mapset):
    assert sm_mapset[0].holds.last_offset() == \
           pytest.approx(2 * 60000 + 45836, abs=2)


def test_hit_count(sm_mapset):
    assert len(sm_mapset[0].hits) == 1816
    assert len(sm_mapset[0].holds) == 47
    assert len(sm_mapset[1].hits) == 2512
    assert len(sm_mapset[1].holds) == 165
