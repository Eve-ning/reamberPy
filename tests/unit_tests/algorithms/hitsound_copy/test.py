from pathlib import Path

from reamber.algorithms.mutate.hitSoundCopy import hitsound_copy
from reamber.osu import OsuMap

THIS_DIR = Path(__file__).parent

EXPECTED_PATH = THIS_DIR / 'expected.osu'
WRITE_PATH = THIS_DIR / 'write.osu'

M_FROM = OsuMap.read_file(THIS_DIR / 'hitsound_src.osu')
M_TO = OsuMap.read_file(THIS_DIR / 'hitsound_target.osu')

def test_hitsound_copy():
    m_out = hitsound_copy(M_FROM, M_TO)
    m_out.write_file(WRITE_PATH)
    with open(EXPECTED_PATH) as f:
        expected = f.read()
    with open(WRITE_PATH) as f:
        actual = f.read()
    assert expected == actual
