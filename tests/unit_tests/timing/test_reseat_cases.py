import numpy as np
import pytest

from reamber.algorithms.timing.TimingMap import TimingMap
from reamber.algorithms.timing.utils.BpmChangeSnap import BpmChangeSnap
from reamber.algorithms.timing.utils.snap import Snap

"""
Cases   0 1 2 3 4 5 6 7 8 9           0 1 2 3 4 5 6 7 8 9
Normal  | - - - | - - - |     |-->|   | - - - | - - - |             
>-|     | - - - o | - - |     |-->|   | - - - | | - - |             
<-|     | - - | o - - - |     |-->|   | - - | | - - - |             
|->     | - - - | - - - o |   |-->|   | - - - | - - - | |            
|-<     | - - - | - - | o     |-->|   | - - - | - - | |              
<-<     | - - | o - - | o     |-->|   | - - | | - - | |              
>->     | - - - o | - - o |   |-->|   | - - - | | - - | |                
>-<     | - - - o | - | o     |-->|   | - - - | | - | |              
<->     | - - | o - - - o |   |-->|   | - - | | - - - | |                
"""


@pytest.mark.parametrize(
    'bc_0',
    (3, 4, 5),
    ids=['<', '-', '>']
)
@pytest.mark.parametrize(
    'bc_1',
    (7, 8, 9),
    ids=['<', '-', '>']
)
def test_reseat(bc_0, bc_1):
    """ In the case where the measures aren't exact, we add a measure. """
    expected = sorted(list({0, 4, 8, bc_0, bc_1}))
    bpms = 60000 / np.diff(expected) * 4
    expected_bcs_s = [BpmChangeSnap(bpm, 4, Snap(e, 0, 4))
                      for e, bpm in enumerate([*bpms, 60000])]
    inp = [0, bc_0, bc_1]
    tm = TimingMap.from_bpm_changes_snap(
        0,
        [BpmChangeSnap(60000, 4, Snap(0, x, 4)) for x in inp]
    )
    assert tm.bpm_changes_snap() == expected_bcs_s
