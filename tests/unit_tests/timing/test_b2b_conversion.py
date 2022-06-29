from copy import deepcopy
from dataclasses import asdict

import pytest

from reamber.algorithms.timing.TimingMap import TimingMap
from tests.unit_tests.timing.cases.test_cases import cases


@pytest.mark.parametrize(
    'case_name,case',
    deepcopy(cases).items(),
)
def test_b2b_conversion(case_name, case):
    tm = TimingMap.from_bpm_changes_offset(case.bpm_changes_offset)
    tm = tm.from_bpm_changes_snap(0, tm.bpm_changes_snap)

    for bco_actual, bco_expected in zip(tm.bpm_changes_offset,
                                        case.bpm_changes_reseat_offset):
        assert bco_actual.bpm == pytest.approx(bco_expected.bpm)
        assert bco_actual.offset == pytest.approx(bco_expected.offset)
        assert bco_actual.metronome == pytest.approx(bco_expected.metronome)
