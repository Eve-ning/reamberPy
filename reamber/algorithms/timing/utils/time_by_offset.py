from __future__ import annotations

from fractions import Fraction
from typing import List

from reamber.algorithms.timing.utils import \
    BpmChangeSnap, BpmChangeOffset

MAX_DENOMINATOR = 100


@staticmethod
def time_by_offset(initial_offset: float,
                   bpm_changes_offset: List[BpmChangeOffset]) -> TimingMap:
    bpm_changes_offset.sort(key=lambda x: x.offset)
    bpm_changes_snap = []
    curr_measure = 0

    for i, j in zip(bpm_changes_offset[:-1], bpm_changes_offset[1:]):
        diff_offset = j.offset - i.offset
        diff_beat = Fraction(
            diff_offset / i.beat_length).limit_denominator(100)
        """ 3 cases
        1) No Change
        2) J is in same measure
        3) J is in different measure
        """
        if diff_beat % i.metronome == 0:
            # Case 1
            bpm_changes_snap.append(
                BpmChangeSnap(bpm=i.bpm,
                              metronome=i.metronome,
                              measure=curr_measure,
                              beat=0,
                              snap=Fraction(0))
            )

            curr_measure += int(diff_beat // i.metronome)

        elif diff_beat < i.metronome:
            # Case 2
            bpm_changes_snap.append(
                BpmChangeSnap(bpm=i.bpm,
                              metronome=Fraction(diff_beat)
                              .limit_denominator(MAX_DENOMINATOR),
                              measure=curr_measure,
                              beat=0,
                              snap=Fraction(0)))
            curr_measure += 1

        else:
            # Case 3
            # We append the original first
            bpm_changes_snap.append(BpmChangeSnap(bpm=i.bpm,
                                                  metronome=i.metronome,
                                                  measure=curr_measure,
                                                  beat=0,
                                                  snap=Fraction(0)))
            curr_measure += int(diff_beat // i.metronome)
            # Then we append the corrector
            metronome = Fraction(diff_beat % i.metronome) \
                .limit_denominator(MAX_DENOMINATOR)
            if metronome:
                bpm_changes_snap.append(BpmChangeSnap(bpm=i.bpm,
                                                      metronome=metronome,
                                                      measure=curr_measure,
                                                      beat=0,
                                                      snap=Fraction(0)))
                curr_measure += 1

    # This algorithm pivots on the snap algorithm.
    bpm_changes_snap.append(BpmChangeSnap(bpm=bpm_changes_offset[-1].bpm,
                                          metronome=
                                          bpm_changes_offset[
                                              -1].metronome,
                                          measure=curr_measure,
                                          beat=0,
                                          snap=Fraction(0)))

    tm = TimingMap.time_by_snap(initial_offset=initial_offset,
                                bpm_changes_snap=bpm_changes_snap)
    # tm._force_bpm_measure()
    return tm
