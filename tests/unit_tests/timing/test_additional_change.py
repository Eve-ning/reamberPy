from reamber.algorithms.timing.TimingMap import TimingMap
from reamber.algorithms.timing.utils.BpmChangeOffset import BpmChangeOffset


def test_additional_change():
    """ In the case where the measures aren't exact, we add a measure. """
    tm = TimingMap.from_bpm_changes_offset(
        [BpmChangeOffset(600, 4, 0),
         BpmChangeOffset(600, 4, 500)]
    )
    tm = tm.from_bpm_changes_snap(0, tm.bpm_changes_snap())
    assert tm.bpm_changes_offset == [
        BpmChangeOffset(600, 4, 0),
        BpmChangeOffset(2400, 4, 400),
        BpmChangeOffset(600, 4, 500)
    ]
