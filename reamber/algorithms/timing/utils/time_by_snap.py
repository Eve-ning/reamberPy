from __future__ import annotations

from fractions import Fraction
from typing import List

from reamber.algorithms.timing import TimingMap
from reamber.algorithms.timing.utils import \
    BpmChange, BpmChangeSnap
from reamber.base.RAConst import RAConst

MAX_DENOMINATOR = 100


def time_by_snap(initial_offset,
                 bpm_changes_snap: List[BpmChangeSnap]) -> TimingMap:
    """ Creates a Timing Map using the BPM Changes provided.

    The first BPM Change MUST be on Measure, Beat, Slot 0.

    :param initial_offset: The offset of the first measure.
    :param bpm_changes_snap: A List of BPM Changes of BpmChangeSnap Class.
    :return:
    """
    bpm_changes_snap.sort(key=lambda x: (x.measure, x.beat, x.snap))
    metronome = metronome_snap(bpm_changes_snap)
    initial = bpm_changes_snap[0]
    assert initial.measure == 0 and \
           initial.beat == 0 and \
           initial.snap == 0, \
        f"The first bpm must be on Measure 0, Beat 0, Slot 0. " \
        f"It is now {initial.measure}, {initial.beat}, {initial.snap}"
    bpm_changes = [
        BpmChange(initial.bpm, initial.metronome, initial_offset,
                  0, Fraction(0), 0, )]

    prev_offset = initial_offset
    prev_bpm = bpm_changes_snap[0].bpm
    prev_beat = Fraction(0)
    prev_slot = Fraction(0)
    prev_measure = 0

    for bpm in bpm_changes_snap[1:]:
        measure = bpm.measure
        beat = bpm.beat
        slot = bpm.snap

        """
            0                             1
        [---|---]                 [---|---|---]
                 [---|---|---|---]
            <-A-><-------B-------><---C--->
        """

        # This is the A, C buffer
        #            <-------------------A----------------------------------->
        diff_beats = metronome[prev_measure] - prev_beat - 1 + (1 - prev_slot) \
                     + beat + slot
        #            + <----C---->
        for i in range(prev_measure + 1, measure):
            # This is the B buffer
            diff_beats += metronome[i]

        for i in range(measure, prev_measure + 1):
            # This is the inverse B buffer
            # This happens when the measures are the same, so this corrects the above formula.
            diff_beats -= metronome[i]

        offset = prev_offset + diff_beats * RAConst.MIN_TO_MSEC / prev_bpm
        bpm_changes.append(
            BpmChange(bpm.bpm, bpm.metronome, offset, bpm.measure,
                      bpm.beat, bpm.snap))

        prev_measure = measure
        prev_offset = offset
        prev_bpm = bpm.bpm
        prev_beat = beat
        prev_slot = slot

    tm = TimingMap(initial_offset=initial_offset,
                   bpm_changes=bpm_changes)
    return tm

def metronome_snap(bpm_changes_snap: List[BpmChangeSnap]):
    """ This function simulates the metronome and generates a list of beats per measure
    used for timing_by_snap. """
    prev_beats = bpm_changes_snap[0].metronome
    prev_measure = 0
    metronome = []
    # We process the number of beats first
    for b in bpm_changes_snap[1:]:
        # Note that beat changes can only happen on measures, which makes sense logically.
        measure = b.measure
        beats = b.metronome

        # For each difference in measure, we append the beats
        diff_measure = measure - prev_measure

        for _ in range(diff_measure):
            metronome.append(prev_beats)

        prev_beats = beats
        prev_measure = measure
    # If last, we push the last beat change
    metronome.append(prev_beats)
    return metronome