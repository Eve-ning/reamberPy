from __future__ import annotations

from dataclasses import field
from fractions import Fraction
from typing import List, Union, Iterable

import numpy as np
import pandas as pd

from reamber.algorithms.timing.utils import \
    BpmChange, BpmChangeSnap, BpmChangeOffset, Snapper
from reamber.base.RAConst import RAConst

MAX_DENOMINATOR = 100


class TimingMap:
    initial_offset: float
    bpm_changes: List[BpmChange] = field(default_factory=lambda x: [])
    snapper: Snapper
    prev_divisions: tuple

    def __init__(self,
                 initial_offset: float,
                 bpm_changes: List[BpmChange]):
        self.initial_offset = initial_offset
        self.bpm_changes = bpm_changes

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

    @staticmethod
    def time_by_snap(initial_offset,
                     bpm_changes_snap: List[BpmChangeSnap]) -> TimingMap:
        """ Creates a Timing Map using the BPM Changes provided.

        The first BPM Change MUST be on Measure, Beat, Slot 0.

        :param initial_offset: The offset of the first measure.
        :param bpm_changes_snap: A List of BPM Changes of BpmChangeSnap Class.
        :return:
        """
        bpm_changes_snap.sort(key=lambda x: (x.measure, x.beat, x.snap))
        metronome = TimingMap._metronome_snap(bpm_changes_snap)
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
            diff_beats = metronome[prev_measure] - prev_beat - 1 + (
                1 - prev_slot) \
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

    @staticmethod
    def _metronome_snap(bpm_changes_snap: List[BpmChangeSnap]):
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

    def _force_bpm_measure(self):
        """ This function forces the bpms to be on measures, this is better supported on all VSRGs.

        However, this will irreversibly remove all BPM sub-measure BPM Changes.
        All note data will be re-snapped.

        The algorithm has 3 parts.

        1) Group By Measure
        2) Add Beat 0, Slot 0s and Calculate Offset
        3) Force Measures

        """

        # Group By Measures
        measures = {}  # Measure: {BPMs}

        for b in self.bpm_changes:
            if b.measure not in measures.keys():
                measures[b.measure] = [b]
            else:
                measures[b.measure].append(b)

        prev_bpm = None
        # Here, we make sure that every measure with a bpm change has a beat=0, snap=0
        for e, bpms in enumerate(measures.values()):
            if bpms[0].beat != 0 or bpms[0].snap != 0:
                diff_beat = (bpms[
                                 0].measure - prev_bpm.measure - 1) * prev_bpm.metronome + \
                            (
                                prev_bpm.metronome - prev_bpm.beat - prev_bpm.snap)
                bpms.insert(
                    0,
                    BpmChange(
                        bpm=prev_bpm.bpm,
                        metronome=bpms[0].metronome,
                        offset=diff_beat * prev_bpm.beat_length + prev_bpm.offset,
                        measure=bpms[0].measure,
                        beat=0,
                        snap=Fraction(0)
                    )
                )
            prev_bpm = bpms[-1]

        # Separate into measures
        measure_push = 0
        for m, bpms in measures.items():
            bpms: List[BpmChange]
            metronome = bpms[0].metronome
            prev_beat = metronome
            for b in bpms:
                b.measure += measure_push
            for i in reversed(range(len(bpms))):
                # This will be run in reverse (it's easier)
                b = bpms[i]
                # The "beat" here is including the fraction slot/snap
                beat = b.beat + b.snap
                diff_beats = prev_beat - beat  # The number of metronome for this
                if diff_beats < 1:
                    b.bpm *= 1 / float(diff_beats)
                    diff_beats = 1
                b.metronome = diff_beats
                b.beat = 0
                b.snap = Fraction(0)
                prev_beat = beat

                if beat != 0:
                    measure_push += 1
                    for j in range(i, len(bpms)):
                        bpms[j].measure += 1

        # Reassign
        self.bpm_changes = [i for j in measures.values() for i in j]

    def offsets(self,
                measures: Union[List, int],
                beats: Union[List, int],
                slots: Union[List[Fraction], Fraction]) -> List[float]:
        """ Finds the offsets in ms for the specified snaps

        :param measures: List of Measures or measure, in integers
        :param beats: List of Beats or beat in integers
        :param slots: List of Slots or slot in Fraction.
        :return: List[float]
        """
        measures = [measures] if isinstance(measures, int) else measures
        beats = [beats] if isinstance(beats, int) else beats
        slots = [slots] if isinstance(slots, (Fraction, float, int)) else slots

        offsets = []

        for measure, beat, slot in zip(measures, beats, slots):
            for b in reversed(self.bpm_changes):
                if b.measure > measure:
                    # If the measure is more, it's definitely not it
                    continue
                if b.measure == measure and b.beat + b.snap > beat + slot:
                    # If the measure is the same, we check if its beat + slot is more
                    continue

                diff_measure = measure - b.measure
                diff_beat = beat - b.beat
                diff_slot = slot - b.snap
                offsets.append(
                    b.offset +
                    (
                        diff_measure * b.metronome + diff_beat + diff_slot) * b.beat_length)
                break

        return offsets

    def snaps(self,
              offsets: Union[Iterable[float], float],
              divisions: Iterable[int] = (
                  1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 16, 32, 48, 64, 96),
              transpose: bool = False) -> List[
        List[int], List[int], List[Fraction]]:
        """ Finds the snaps from the provided offsets

        :param offsets: Offsets to find snaps
        :param divisions: Divisions for the snap to conform to.
        :param transpose: Transposes the returned List
        :return: List[Tuple(Measure), Tuple(Beat), Tuple(Slot)] if transpose List[Tuple(Measure, Beat, Slot)]
        """

        snaps = [[], [], []]
        offsets = [offsets] if isinstance(offsets, (int, float)) else offsets

        if not self.snapper or self.prev_divisions != divisions:
            # noinspection PyTypeChecker
            self.prev_divisions = divisions
            self.snapper = TimingMap.Slotter(divisions)

        # This is required as the TimingMap modulus is prone to rounding errors
        # e.g. 3.9999 -> measure 3, beat 4, snap 191/192
        # This will correct it to 4.0 without exceeding to snap 1/192
        DIVISION_CORRECTION = 0.001
        for offset in offsets:
            for b in reversed(self.bpm_changes):
                if b.offset > offset: continue

                diff_offset = offset - b.offset
                beats_total = diff_offset / b.beat_length + DIVISION_CORRECTION
                measure = int(beats_total // b.metronome)
                beat = int(beats_total - measure * b.metronome)
                slot = self.snapper.slot(beats_total % 1)
                snaps[0].append(b.measure + measure)
                snaps[1].append(b.beat + beat)
                snaps[2].append(b.snap + slot)
                break

        return list(zip(*snaps)) if transpose else snaps

    def snap_objects(self,
                     offsets: Iterable[float],
                     objects: Iterable[object]):
        a = pd.DataFrame([*self.snaps(offsets), objects]).T
        a.columns = ['measure', 'beat', 'slot', 'obj']
        a.measure = pd.to_numeric(a.measure)
        a.beat = pd.to_numeric(a.beat)

        return a

    @staticmethod
    def _reduce_exact_limit(a: List, threshold: int) -> list:
        """ Given a list of denominators, it reduces the required amount of cells needed to fully hold them exactly

        Take for example, [1,3,6,7] with a limit of 10
        The best way to reduce it would be to use [6,7]. as we can represent 1, 3, 6 with 6 slots.

        The limit depicts the highest value it can be.

        The algorithm is simple, it loops through the whole list in a cartesian pair-wise and tries to combine pairs
        with LCM as long as it doesn't exceed the threshold.

        The return is a dictionary on the reduction. For example the above will yield
        {1: 6, 3: 6, 6: 6, 7: 7}

        :param a: The list to reduce
        :param threshold: The threshold to not exceed when reducing
        :return: A dictionary mapping on how it is reduced.
        """
        a_ = [0 for _ in a]
        length = len(a)
        for i in range(length):
            for j in range(length):
                if i == j: continue
                b, c = a[i], a[j]
                if b is None or c is None: continue
                lcm = np.lcm(b, c)
                if lcm < threshold:
                    a[i] = lcm
                    a_[j] = lcm
                    a[j] = None

        for i in range(length):
            if a_[i] == 0:
                a_[i] = a[i]

        return a_
