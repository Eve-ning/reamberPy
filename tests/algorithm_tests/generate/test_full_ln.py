import numpy as np
import pytest

from reamber.algorithms.generate import full_ln
from reamber.base.Map import Map
from reamber.base.lists.notes.HitList import HitList
from reamber.base.lists.notes.HoldList import HoldList

GAP = 150
LN_AS_HIT = 100

# MIN_DIST is the smallest difference before it's transformed to a hit
MIN_DIST = GAP + LN_AS_HIT


@pytest.mark.parametrize(
    'hit_offsets, hold_offsets, hold_lengths, '
    'exp_hit_offsets, exp_hold_offsets, exp_hold_lengths',
    [
        ([0, MIN_DIST], [], [],
         [MIN_DIST], [0], [LN_AS_HIT]),
        ([0, MIN_DIST - 1], [], [],
         [0, MIN_DIST - 1], [], []),
        ([], [0, MIN_DIST], [100, 100],
         [], [0, MIN_DIST], [LN_AS_HIT, 100]),
        ([], [0, MIN_DIST - 1], [100, 100],
         [0], [MIN_DIST - 1], [100]),
        ([0], [MIN_DIST], [100],
         [], [0, MIN_DIST], [LN_AS_HIT, 100]),
        ([MIN_DIST], [0], [100],
         [MIN_DIST], [0], [LN_AS_HIT]),
    ],
    ids=['Hit-Hit', 'Hit-Hit(Mini LN)', 'Hold-Hold', 'Hold-Hold(Mini LN)',
         'Hit-Hold', 'Hold-Hit']

)
def test_full_ln(hit_offsets, hold_offsets, hold_lengths,
                 exp_hit_offsets, exp_hold_offsets, exp_hold_lengths):
    m = Map()
    m.hits = HitList.from_dict({'offset': hit_offsets, })
    m.holds = HoldList.from_dict({'offset': hold_offsets,
                                  'length': hold_lengths})
    m_out = full_ln(m, GAP, LN_AS_HIT)
    assert np.all(m_out.hits.offset == exp_hit_offsets)
    assert np.all(m_out.holds.offset == exp_hold_offsets)
    assert np.all(m_out.holds.length == exp_hold_lengths)
