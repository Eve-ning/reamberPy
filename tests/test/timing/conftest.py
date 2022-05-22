from typing import List, Tuple

import pytest

from reamber.algorithms.timing.utils.BpmChangeOffset import BpmChangeOffset
from reamber.algorithms.timing.utils.BpmChangeSnap import BpmChangeSnap
from reamber.algorithms.timing.utils.snap import Snap

C = 60000


@pytest.fixture
def scenario_1() -> Tuple[List[BpmChangeOffset], List[BpmChangeSnap]]:
    bpm_changes_offset = [
        BpmChangeOffset(C / 100, 4, 0),
        BpmChangeOffset(C / 100, 4, 400)
    ]
    bpm_changes_snap = [
        BpmChangeSnap(C / 100, 4, Snap(0, 0, 0)),
        BpmChangeSnap(C / 100, 4, Snap(1, 0, 0))
    ]
    return bpm_changes_offset, bpm_changes_snap
