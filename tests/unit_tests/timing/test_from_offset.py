from copy import deepcopy

import pytest

from reamber.algorithms.timing.TimingMap import TimingMap
from tests.unit_tests.timing.cases.test_cases import cases


@pytest.mark.parametrize(
    'case_name,case',
    deepcopy(cases).items(),
)
def test_from_offset(case_name,case):
    tm = TimingMap.from_bpm_changes_offset(case.bpm_changes_offset)
    assert tm.bpm_changes_offset == case.bpm_changes_offset
