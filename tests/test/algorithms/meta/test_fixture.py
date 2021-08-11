import os
import pytest

from reamber.osu.OsuMap import OsuMap

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

SRC = os.path.join(THIS_DIR, 'hitsound_src.osu')
TGT = os.path.join(THIS_DIR, 'hitsound_target.osu')

@pytest.fixture(scope='package')
def src() -> OsuMap:
    return OsuMap.read_file(SRC)

@pytest.fixture(scope='package')
def tgt() -> OsuMap:
    return OsuMap.read_file(TGT)
