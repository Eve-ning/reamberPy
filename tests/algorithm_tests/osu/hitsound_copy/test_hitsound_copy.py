from pathlib import Path

from reamber.algorithms.osu.hitsound_copy import hitsound_copy
from reamber.osu import OsuMap

THIS_DIR = Path(__file__).parent

EXPECTED_PATH = THIS_DIR / 'expected.osu'

M_FROM = OsuMap.read_file(THIS_DIR / 'hitsound_src.osu')
M_TO = OsuMap.read_file(THIS_DIR / 'hitsound_target.osu')


def test_hitsound_copy():
    m_out = hitsound_copy(M_FROM, M_TO)
    with open(EXPECTED_PATH) as f:
        expected = f.read()
    assert expected == "\n".join(m_out.write())
