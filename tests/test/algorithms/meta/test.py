
from reamber.algorithms.mutate.hitSoundCopy import hitsound_copy
from reamber.osu.OsuMap import OsuMap
from tests.test.RSC_PATHS import *
from tests.test.algorithms.meta.test_fixture import src, tgt


def test_osu2(src, tgt):
    m_out = hitsound_copy(m_from=src, m_to=tgt)
    m_out.write_file("out.osu")


