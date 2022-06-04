import pytest

from reamber.algorithms.timing.TimingMap import TimingMap
from tests.test.timing.test_cases import cases, cases_id


@pytest.mark.parametrize(
    'case',
    cases,
    ids=cases_id
)
def test_reseat(case):
    assert case.bpm_changes_reseat_snap == \
           TimingMap.reseat_bpm_changes_snap(case.bpm_changes_snap)
