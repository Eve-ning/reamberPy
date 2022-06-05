import pytest

from reamber.algorithms.timing.TimingMap import TimingMap
from tests.test.timing.test_cases import cases, cases_id


@pytest.mark.parametrize(
    'case',
    cases,
    ids=cases_id
)
def test_from_snap(case):
    tm = TimingMap.from_bpm_changes_snap(0, case.bpm_changes_snap)
    assert tm.bpm_changes_offset == case.bpm_changes_reseat_offset