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
