from collections import namedtuple
from dataclasses import dataclass, field
from fractions import Fraction
from typing import List, Union, Tuple

import numpy as np
import pandas as pd

from reamber.base import RAConst


@dataclass
class BpmChangeSnap:
    bpm: float
    measure: int
    beat: int
    beats_per_measure: int
    slot: Fraction
@dataclass
class BpmChangeOffset:
    bpm: float
    beats_per_measure: int
    offset: float
@dataclass
class BpmChange:
    bpm: float
    beats_per_measure: int
    offset: float
    measure: int
    beat: int
    slot: Fraction

class TimingMap:

    initial_bpm: float
    initial_offset: float
    bpm_changes: List[BpmChange] = field(default_factory=lambda x: [])

    def __init__(self,
                 initial_bpm: float,
                 initial_offset: float,
                 bpm_changes: List[BpmChange]):
        self.initial_bpm = initial_bpm
        self.initial_offset = initial_offset
        self.bpm_changes = bpm_changes

    @staticmethod
    def time_by_snap(initial_bpm: float,
                     initial_offset: float,
                     initial_beats: int,
                     bpm_changes_snap: List[BpmChangeSnap]):

        beats_per_measure = TimingMap._beats_per_measure_snap(initial_beats, bpm_changes_snap)
        bpm_changes = [BpmChange(initial_bpm, initial_beats, initial_offset, 0, 0, Fraction(0))]

        prev_offset = initial_offset
        prev_bpm = initial_bpm
        prev_beat = Fraction(0, 1)
        prev_slot = Fraction(0, 1)
        prev_measure = 0

        for bpm in bpm_changes_snap:
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

        return TimingMap(initial_bpm=initial_bpm,
                         initial_offset=initial_offset,
                         bpm_changes=bpm_changes)


    @staticmethod
    def _beats_per_measure_snap(initial_beats: int,
                                bpm_changes_snap: List[BpmChangeSnap]):
        """ This function simulates the beats_per_measure and generates a list used for timing_by_snap. """
        prev_beats = initial_beats
        prev_measure = 0
        beats_per_measure = []
        # We process the number of beats first
        for b in bpm_changes_snap:
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

        However, this will irreversibly remove all BPM sub-measure BPM Changes, though, will not affect
        note data.

        Case 1:

        200
        [---|---|---|---][---|-*|-|-]
                               400
        [---|---|---|---][-|||][-|||][--
        200              533   640   400
        """

        changes = len(self.bpm_changes)
        for a, b in zip(range(0, changes - 1), range(1, changes)):
            i, j = self.bpm_changes[a], self.bpm_changes[b]
            # We don't care about the snapped ones
            if j.beat == 0 and j.slot == Fraction(0):
                continue

            # It is guaranteed that i is on a measure.
            # j is then either on beat or on snap.
            if i.measure != j.measure:
                # If both are on different snaps, we create an additional change on
                add_offset = (j.measure - i.measure) * RAConst.MIN_TO_MSEC / i.bpm

                # Frac = How far in the j.beat / j.slot in the measure.
                # [---|-------]
                frac = j.beat + j.slot
                additional = BpmChange(bpm=i.bpm / frac,
                                       beats_per_measure=i.beats_per_measure,
                                       offset=add_offset,
                                       measure=j.measure,
                                       beat=0,
                                       slot=Fraction(0))

                j.bpm /= 1 - frac

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
                if b.measure > measure or b.beat > beat or b.slot > slot:
                    continue
                diff_measure = measure - b.measure
                diff_beat    = beat - b.beat
                diff_slot    = slot - b.slot
                offsets.append(
                    b.offset +
                    (diff_measure * b.beats_per_measure + diff_beat + diff_slot) * RAConst.MIN_TO_MSEC / b.bpm)
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
                beats_total = diff_offset / (RAConst.MIN_TO_MSEC / b.bpm)
                measure = int(beats_total // b.beats_per_measure)
                beat = int(beats_total - measure)
                slot = slotter.slot(beats_total % 1)
                snaps.append((b.measure + measure,
                              b.beat + beat,
                              b.slot + slot))
                break
        return snaps

    @staticmethod
    def time_by_offset(initial_bpm: float,
                       initial_offset: float,
                       initial_beats: int,
                       bpm_changes_offset: List[BpmChangeOffset]):
        bpm_changes = [BpmChange(initial_bpm, initial_beats, initial_offset, 0, 0, Fraction(0))]
        prev_bpm = initial_bpm

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

