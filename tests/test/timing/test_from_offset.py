import pytest

from reamber.algorithms.timing.TimingMap import TimingMap
from tests.test.timing.test_cases import cases


@pytest.mark.parametrize(
    'case',
    cases
)
def test_from_offset(case):
    tm = TimingMap.from_bpm_changes_offset(case.bpm_changes_offset)
    assert tm.bpm_changes_offset == case.bpm_changes_offset
