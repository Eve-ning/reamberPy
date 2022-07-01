from copy import deepcopy

import pytest

from reamber.algorithms.timing.TimingMap import TimingMap
from tests.unit_tests.timing.cases.test_cases import cases


@pytest.mark.parametrize(
    'case_name,case',
    deepcopy(cases).items(),
)
def test_reseat(case_name, case):
    assert TimingMap.reseat_bpm_changes_snap(case.bpm_changes_snap) == \
           case.bpm_changes_reseat_snap
