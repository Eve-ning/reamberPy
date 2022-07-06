import numpy as np
import pytest

from reamber.algorithms.timing.TimingMap import TimingMap
from reamber.algorithms.timing.utils.BpmChangeSnap import BpmChangeSnap
from reamber.algorithms.timing.utils.snap import Snap

"""
Cases   0 1 2 3 4 5 6 7 8 9           0 1 2 3 4 5 6 7 8 9
Normal  | - - - | - - - |     |-->|   | - - - | - - - |             
>-|     | - - - o | - - |     |-->|   | - - - | | - - |             
<-|     | - - | o - - - |     |-->|   | - - | - - - | |             
|->     | - - - | - - - o |   |-->|   | - - - | - - - | |            
|-<     | - - - | - - | o     |-->|   | - - - | - - |               
<-<     | - - | - - - | o     |-->|   | - - | - - - |               
>->     | - - - o | - - - |   |-->|   | - - - | | - - - |                
>-<     | - - - o | - | o     |-->|   | - - - | | - |               
<->     | - - | o - - - o |   |-->|   | - - | - - - | - |                
"""


@pytest.mark.parametrize(
    'i, o',
    [
        [(0, 4, 8), (0, 4, 8)],
        [(0, 5, 8), (0, 4, 5, 8)],
        [(0, 3, 8), (0, 3, 7, 8)],
        [(0, 4, 9), (0, 4, 8, 9)],
        [(0, 4, 7), (0, 4, 7)],
        [(0, 3, 7), (0, 3, 7)],
        [(0, 5, 9), (0, 4, 5, 9)],
        [(0, 5, 7), (0, 4, 5, 7)],
        [(0, 3, 9), (0, 3, 7, 9)],
    ],
    ids=["Normal", ">-|", "<-|", "|->", "|-<", "<-<", ">->", ">-<", "<->"]
)
def test_reseat(i, o):
    """ In the case where the measures aren't exact, we add a measure. """
    bpms = 60000 / np.diff(o) * 4
    expected_bcs_s = [BpmChangeSnap(bpm, 4, Snap(e, 0, 4))
                      for e, bpm in enumerate([*bpms, 60000])]

    bcs_s = TimingMap.reseat_bpm_changes_snap(
        [BpmChangeSnap(60000, 4, Snap(0, x, 4)) for x in i]
    )
    assert bcs_s == expected_bcs_s


def test_reseat_approx_late():
    """ In the case where the measures aren't exact, we add a measure. """

    tm = TimingMap.from_bpm_changes_snap(
        0,
        [BpmChangeSnap(60000, 4, Snap(0, 0, 4)),
         BpmChangeSnap(60000, 4, Snap(1, 0.0001, 4)),
         BpmChangeSnap(60000, 4, Snap(2, 0, 4))]
    )
    assert [bco.offset for bco in tm.bpm_changes_offset] == [0, 4.0001, 8]


def test_reseat_approx_early():
    """ In the case where the measures aren't exact, we add a measure. """

    tm = TimingMap.from_bpm_changes_snap(
        0,
        [
            BpmChangeSnap(60000, 4, Snap(0, 0, 4)),
            BpmChangeSnap(60000, 4, Snap(0, 3.9999, 4)),
            BpmChangeSnap(60000, 4, Snap(2, 0, 4))
        ]
    )
    assert [bco.offset for bco in tm.bpm_changes_offset] == [0, 3.9999, 8]
