
from reamber.algorithms.mutate.hitSoundCopy import hitsound_copy
from reamber.osu.OsuMap import OsuMap
from tests.test.RSC_PATHS import *
from tests.test.algorithms.meta.test_fixture import src, tgt

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

MAP_WRITE_EXP = os.path.join(THIS_DIR, 'expected.osu')
MAP_WRITE = os.path.join(THIS_DIR, 'write.osu')


def test_osu2(src, tgt):
    m_out = hitsound_copy(m_from=src, m_to=tgt)
    m_out.write_file(MAP_WRITE)
    with open(MAP_WRITE_EXP) as f:
        expected = f.read()
    with open(MAP_WRITE) as f:
        actual = f.read()
    if expected != actual:
        assert False
