from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
from typing import List, Union, Tuple

import numpy as np

from reamber.base import RAConst


@dataclass
class BpmChangeSnap:
    bpm: float
    measure: int
    beat: int
    slot: Fraction
    beats_per_measure: Union[Fraction, float]

    @property
    def beat_length(self) -> float:
        return RAConst.MIN_TO_MSEC / self.bpm

@dataclass
class BpmChangeOffset:
    bpm: float
    beats_per_measure: Union[Fraction, float]
    offset: float

    @property
    def beat_length(self) -> float:
        return RAConst.MIN_TO_MSEC / self.bpm

@dataclass
class BpmChange:
    bpm: float
    beats_per_measure: Union[Fraction, float]
    offset: float
    measure: int
    beat: int
    slot: Fraction

    @property
    def beat_length(self) -> float:
        return RAConst.MIN_TO_MSEC / self.bpm


class TimingMap:

    initial_offset: float
    bpm_changes: List[BpmChange] = field(default_factory=lambda x: [])

    def __init__(self,
                 initial_offset: float,
                 bpm_changes: List[BpmChange]):
        self.initial_offset = initial_offset
        self.bpm_changes = bpm_changes

    @staticmethod
    def time_by_offset(initial_offset: float,
                       bpm_changes_offset: List[BpmChangeOffset]) -> TimingMap:
        bpm_changes_snap = []
        curr_measure = 0

        for i, j in zip(bpm_changes_offset[:-1], bpm_changes_offset[1:]):
            diff_offset = j.offset - i.offset
            diff_beat = diff_offset / i.beat_length
            """ 3 cases
            1) No Change
            2) J is in same measure
            3) J is in different measure
            """
            if diff_beat % i.beats_per_measure == 0:
                # Case 1
                bpm_changes_snap.append(BpmChangeSnap(bpm=i.bpm,
                                                      beats_per_measure=i.beats_per_measure,
                                                      measure=curr_measure,
                                                      beat=0,
                                                      slot=Fraction(0)))

                curr_measure += int(diff_beat // i.beats_per_measure)
            elif diff_beat < i.beats_per_measure:
                # Case 2
                bpm_changes_snap.append(BpmChangeSnap(bpm=i.bpm,
                                                      beats_per_measure=Fraction(diff_beat),
                                                      measure=curr_measure,
                                                      beat=0,
                                                      slot=Fraction(0)))
                curr_measure += 1

            else:
                # Case 3
                # We append the original first
                bpm_changes_snap.append(BpmChangeSnap(bpm=i.bpm,
                                                      beats_per_measure=i.beats_per_measure,
                                                      measure=curr_measure,
                                                      beat=0,
                                                      slot=Fraction(0)))
                curr_measure += int(diff_beat // i.beats_per_measure)
                # Then we append the corrector
                bpm_changes_snap.append(BpmChangeSnap(bpm=i.bpm,
                                                      beats_per_measure=Fraction(diff_beat % 1),
                                                      measure=curr_measure,
                                                      beat=0,
                                                      slot=Fraction(0)))
                curr_measure += 1

        # This algorithm pivots on the snap algorithm.
        bpm_changes_snap.append(BpmChangeSnap(bpm=bpm_changes_offset[-1].bpm,
                                              beats_per_measure=bpm_changes_offset[-1].beats_per_measure,
                                              measure=curr_measure,
                                              beat=0,
                                              slot=Fraction(0)))

        tm = TimingMap.time_by_snap(initial_offset=initial_offset,
                                    bpm_changes_snap=bpm_changes_snap)
        tm._force_bpm_measure()
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
        beats_per_measure = TimingMap._beats_per_measure_snap(bpm_changes_snap)
        initial = bpm_changes_snap[0]
        assert initial.measure == 0 and \
               initial.beat == 0 and \
               initial.slot == 0,\
            f"The first bpm must be on Measure 0, Beat 0, Slot 0. " \
            f"It is now {bpm_changes_snap[0].measure}, {bpm_changes_snap[0].beat}, {bpm_changes_snap[0].slot}"
        bpm_changes = [BpmChange(initial.bpm, initial.beats_per_measure, initial_offset,
                                 0, 0, Fraction(0))]

        prev_offset = initial_offset
        prev_bpm = bpm_changes_snap[0].bpm
        prev_beat = Fraction(0)
        prev_slot = Fraction(0)
        prev_measure = 0

        for bpm in bpm_changes_snap[1:]:
            measure = bpm.measure
            beat = bpm.beat
            slot = bpm.slot

            """
                0                             1
            [---|---]                 [---|---|---]
                     [---|---|---|---]
                <-A-><-------B-------><---C--->
            """

            # This is the A, C buffer
            #            <---------------------------------A-----------------------------> + <----C---->
            diff_beats = beats_per_measure[prev_measure] - prev_beat - 1 + (1 - prev_slot) + beat + slot
            for i in range(prev_measure + 1, measure):
                # This is the B buffer
                diff_beats += beats_per_measure[i]

            for i in range(measure, prev_measure + 1):
                # This is the inverse B buffer
                # This happens when the measures are the same, so this corrects the above formula.
                diff_beats -= beats_per_measure[i]

            offset = prev_offset + diff_beats * RAConst.MIN_TO_MSEC / prev_bpm
            bpm_changes.append(BpmChange(bpm.bpm, bpm.beats_per_measure, offset, bpm.measure, bpm.beat, bpm.slot))

            prev_measure = measure
            prev_offset = offset
            prev_bpm = bpm.bpm
            prev_beat = beat
            prev_slot = slot

        tm = TimingMap(initial_offset=initial_offset,
                         bpm_changes=bpm_changes)
        return tm

    @staticmethod
    def _beats_per_measure_snap(bpm_changes_snap: List[BpmChangeSnap]):
        """ This function simulates the beats_per_measure and generates a list of beats per measure
        used for timing_by_snap. """
        prev_beats = bpm_changes_snap[0].beats_per_measure
        prev_measure = 0
        beats_per_measure = []
        # We process the number of beats first
        for b in bpm_changes_snap[1:]:
            # Note that beat changes can only happen on measures, which makes sense logically.
            measure = b.measure
            beats = b.beats_per_measure

            # For each difference in measure, we append the beats
            diff_measure = measure - prev_measure

            for _ in range(diff_measure):
                beats_per_measure.append(prev_beats)

            prev_beats = beats
            prev_measure = measure
        # If last, we push the last beat change
        beats_per_measure.append(prev_beats)
        return beats_per_measure

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
        # Here, we make sure that every measure with a bpm change has a beat=0, slot=0
        for e, bpms in enumerate(measures.values()):
            if bpms[0].beat != 0 or bpms[0].slot != 0:
                diff_beat = (bpms[0].measure - prev_bpm.measure - 1) * prev_bpm.beats_per_measure + \
                            (prev_bpm.beats_per_measure - prev_bpm.beat - prev_bpm.slot)
                bpms.insert(0, BpmChange(bpm=prev_bpm.bpm,
                                         beats_per_measure=bpms[0].beats_per_measure,
                                         offset=diff_beat * prev_bpm.beat_length + prev_bpm.offset,
                                         measure=bpms[0].measure,
                                         beat=0,
                                         slot=Fraction(0)))
            prev_bpm = bpms[-1]

        # Separate into measures
        measure_push = 0
        for m, bpms in measures.items():
            bpms: List[BpmChange]
            beats_per_measure = bpms[0].beats_per_measure
            prev_beat = beats_per_measure
            for b in bpms:
                b.measure += measure_push
            for i in reversed(range(len(bpms))):
                # This will be run in reverse (it's easier)
                b = bpms[i]
                # The "beat" here is including the fraction slot/snap
                beat = b.beat + b.slot
                diff_beats = prev_beat - beat  # The number of beats_per_measure for this
                b.beats_per_measure = diff_beats
                b.beat = 0
                b.slot = Fraction(0)
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
                    continue
                if b.measure == measure and b.beat + b.slot > beat + slot:
                    continue

                diff_measure = measure - b.measure
                diff_beat    = beat - b.beat
                diff_slot    = slot - b.slot
                offsets.append(
                    b.offset +
                    (diff_measure * b.beats_per_measure + diff_beat + diff_slot) * b.beat_length)
                break

        return offsets

    def snaps(self,
              offsets: Union[List[float], float],
              divisions: List[int] = (1,2,3,4,5,6,7,8,9,12,16,32,64,96)) -> List[Tuple[int, int, Fraction]]:
        """ Finds the snaps from the provided offsets

        :param offsets: Offsets to find snaps
        :param divisions: Divisions for the snap to conform to.
        :return: List[Tuple(Measure, Beat, Slot)]
        """

        snaps = []
        offsets = [offsets] if isinstance(offsets, (int, float)) else offsets
        slotter = self.Slotter(divisions=divisions)

        for offset in offsets:
            for b in reversed(self.bpm_changes):
                if b.offset > offset:
                    continue
                diff_offset = offset - b.offset
                beats_total = diff_offset / b.beat_length
                measure = int(beats_total // b.beats_per_measure)
                beat = int(beats_total - measure * b.beats_per_measure)
                slot = slotter.slot(beats_total % 1)
                snaps.append((b.measure + measure,
                              b.beat + beat,
                              b.slot + slot))
                break
        return snaps

    class Slotter:
        def __init__(self,
                     divisions: List[int]):
            divisions = np.asarray(divisions)
            max_slots = max(divisions)

            # Creates the division triangle
            ar = np.zeros([max_slots, max_slots])
            for i in range(max_slots):
                ar[i, :i + 1] = np.linspace(0, 1, i + 1, endpoint=False)

            # Prunes the repeated slots
            visited = []
            for i in range(max_slots):
                for j in range(max_slots):
                    if ar[i, j] in visited:
                        ar[i, j] = np.nan
                    else:
                        visited.append(ar[i, j])

            ar = np.stack([ar, *np.indices(ar.shape)])[:, divisions - 1]
            self.ar = ar[:, ~np.isnan(ar[0])].T

        def slot(self, frac: float):
            closest = self.ar[np.argmin(np.abs(self.ar[:, 0] - frac))]
            return Fraction(int(closest[2]), int(closest[1] + 1))
