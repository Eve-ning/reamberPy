from __future__ import annotations

from dataclasses import field
from fractions import Fraction
from typing import List, Union, Iterable

import pandas as pd

from reamber.algorithms.timing.utils import BpmChange, Snapper

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

    def offsets(self,
                measures:List | int,
                beats:List | int,
                snaps:List[Fraction] | Fraction) -> List[float]:
        """ Finds the offsets in ms for the specified snaps

        Args:
            measures: Measures in integers
            beats: Beats in integers
            snaps: Slots in Fraction.
        """
        measures = [measures] if isinstance(measures, int) else measures
        beats = [beats] if isinstance(beats, int) else beats
        snaps = [snaps] if isinstance(snaps, (Fraction, float, int)) else snaps

        offsets = []

        for measure, beat, slot in zip(measures, beats, snaps):
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
              offsets: Iterable[float] | float,
              divisions: Iterable[int] = (
                  1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 16, 32, 48, 64, 96),
              transpose: bool = False) -> \
        List[List[int], List[int], List[Fraction]]:
        """ Finds the snaps from the provided offsets

        Args:
            offsets: Offsets to snap
            divisions: Divisions for snapping
            transpose: Transposes the returned List

        Returns:
            List[Tuple(Measure), Tuple(Beat), Tuple(Slot)]
            if transpose List[Tuple(Measure, Beat, Slot)]
        """

        snaps = [[], [], []]
        offsets = [offsets] if isinstance(offsets, (int, float)) else offsets

        if not self.snapper or self.prev_divisions != divisions:
            # noinspection PyTypeChecker
            self.prev_divisions = divisions
            self.snapper = Snapper(divisions)

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
                slot = self.snapper.snap(beats_total % 1)
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
