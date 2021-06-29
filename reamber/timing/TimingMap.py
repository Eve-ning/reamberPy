from collections import namedtuple
from dataclasses import dataclass, field
from fractions import Fraction
from typing import List, Union

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

    @staticmethod
    def time_by_offset(initial_bpm: float,
                       initial_offset: float,
                       initial_beats: int,
                       bpm_changes_offset: List[BpmChangeOffset]):
        bpm_changes = [BpmChange(initial_bpm, initial_beats, initial_offset, 0, 0, Fraction(0))]
        prev_bpm = initial_bpm

